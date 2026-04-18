# management/commands/verify_stats.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from itertools import groupby
from coinflipper.models import CoinFlip, CoinFlipStats


class Command(BaseCommand):
    help = 'Verify and optionally resync coin flip stats'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Resync stats if discrepancy found'
        )

    def handle(self, *args, **options):
        counts = {
            row['result']: row['count']
            for row in CoinFlip.objects.values('result').annotate(count=Count('result'))
        }
        heads = counts.get('H', 0)
        tails = counts.get('T', 0)
        unknown = counts.get('U', 0)
        total = heads + tails + unknown

        results = list(
            CoinFlip.objects.exclude(result='U')
            .order_by('id')
            .values_list('result', flat=True)
        )

        longest_heads = longest_tails = 0
        for key, group in groupby(results):
            run = sum(1 for _ in group)
            if key == 'H':
                longest_heads = max(longest_heads, run)
            elif key == 'T':
                longest_tails = max(longest_tails, run)

        current_run_result = 'U'
        current_run_length = 0
        if results:
            current_run_result = results[-1]
            for key, group in groupby(reversed(results)):
                current_run_length = sum(1 for _ in group)
                break

        stats = CoinFlipStats.get()
        discrepancies = []

        checks = {
            'total': (stats.total, total),
            'heads': (stats.heads, heads),
            'tails': (stats.tails, tails),
            'unknown': (stats.unknown, unknown),
            'longest_run_heads': (stats.longest_run_heads, longest_heads),
            'longest_run_tails': (stats.longest_run_tails, longest_tails),
            'current_run_result': (stats.current_run_result, current_run_result),
            'current_run_length': (stats.current_run_length, current_run_length),
        }

        for field, (stored, calculated) in checks.items():
            if stored != calculated:
                discrepancies.append(
                    f'{field}: stored={stored}, calculated={calculated}'
                )

        if not discrepancies:
            self.stdout.write(self.style.SUCCESS('Stats are accurate.'))
        else:
            self.stdout.write(self.style.WARNING('Discrepancies found:'))
            for d in discrepancies:
                self.stdout.write(f'  {d}')

            if options['fix']:
                with transaction.atomic():
                    stats.total = total
                    stats.heads = heads
                    stats.tails = tails
                    stats.unknown = unknown
                    stats.longest_run_heads = longest_heads
                    stats.longest_run_tails = longest_tails
                    stats.current_run_result = current_run_result
                    stats.current_run_length = current_run_length
                    stats.save()
                self.stdout.write(self.style.SUCCESS('Stats resynced.'))
            else:
                self.stdout.write('Run with --fix to resync.')