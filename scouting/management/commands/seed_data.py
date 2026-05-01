from django.core.management.base import BaseCommand

from scouting.models import Player, ScoutingReport, SkillGrade, Team


class Command(BaseCommand):
    help = 'Seed 2026 mock board data for the scouting database'

    def handle(self, *args, **options):
        SkillGrade.objects.all().delete()
        ScoutingReport.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()

        team_data = [
            ('Kansas', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/9/97/Kansas_Jayhawks_logo.svg/512px-Kansas_Jayhawks_logo.svg.png'),
            ('BYU', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/5/50/BYU_Cougars_logo.svg/512px-BYU_Cougars_logo.svg.png'),
            ('Duke', 'East', 'United States', 'https://a.espncdn.com/i/teamlogos/ncaa/500/150.png'),
            ('North Carolina', 'East', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/2/25/North_Carolina_Tar_Heels_logo.svg/512px-North_Carolina_Tar_Heels_logo.svg.png'),
            ('Houston', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/2/28/Houston_Cougars_logo.svg/512px-Houston_Cougars_logo.svg.png'),
            ('Louisville', 'East', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/1/16/Louisville_Cardinals_wordmark.svg/512px-Louisville_Cardinals_wordmark.svg.png'),
            ('Arkansas', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/6/67/Arkansas_Razorbacks_logo.svg/512px-Arkansas_Razorbacks_logo.svg.png'),
            ('Illinois', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/9/91/Illinois_Fighting_Illini_logo.svg/512px-Illinois_Fighting_Illini_logo.svg.png'),
            ('Washington', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/9/93/Washington_Huskies_logo.svg/512px-Washington_Huskies_logo.svg.png'),
            ('UConn', 'East', 'United States', 'https://upload.wikimedia.org/wikipedia/en/b/b0/Connecticut_Huskies_logo.svg'),
            ('Arizona', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/9/9d/Arizona_Wildcats_logo.svg/512px-Arizona_Wildcats_logo.svg.png'),
            ('Alabama', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Alabama_Crimson_Tide_logo.svg/512px-Alabama_Crimson_Tide_logo.svg.png'),
            ('Tennessee', 'East', 'United States', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Tennessee_Volunteers_logo.svg/512px-Tennessee_Volunteers_logo.svg.png'),
            ('NZ Breakers (NBL)', 'Intl', 'New Zealand', 'https://upload.wikimedia.org/wikipedia/en/thumb/5/53/New_Zealand_Breakers_logo.svg/512px-New_Zealand_Breakers_logo.svg.png'),
            ('Michigan', 'East', 'United States', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Michigan_Wolverines_logo.svg/512px-Michigan_Wolverines_logo.svg.png'),
            ('USC', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/USC_Trojans_logo.svg/512px-USC_Trojans_logo.svg.png'),
            ('Texas', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Texas_Longhorns_logo.svg/512px-Texas_Longhorns_logo.svg.png'),
            ('Baylor', 'West', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Baylor_Bears_logo.svg/512px-Baylor_Bears_logo.svg.png'),
        ]
        teams = {
            name: Team.objects.create(name=name, conference=conf, country=country, logo_url=logo)
            for name, conf, country, logo in team_data
        }

        board = [
            (1, 'Darryn', 'Peterson', 'SG', '6-5', 195, 19, 'Kansas', 'superstar', 'Kobe lite, Ray Allen', 'Keeping Peterson at no.1 based on his full scouting history and top-end flashes despite an unusual season and health concerns.'),
            (2, 'AJ', 'Dybantsa', 'SF', '6-9', 210, 19, 'BYU', 'superstar', 'Tracy McGrady', 'Fierce competitor with elite tools and aggressive downhill pressure who has made a serious case for no.1.'),
            (3, 'Cameron', 'Boozer', 'PF', '6-9', 250, 19, 'Duke', 'superstar', 'Michael Beasley, Al Horford, Kevin Love', 'Efficient, complete offensive machine with can’t-miss feel and star-level projection.'),
            (4, 'Caleb', 'Wilson', 'PF', '6-10', 205, 19, 'North Carolina', 'all_star', 'Kevin Garnett, Shareef Abdur-Rahim', 'Already highly productive with clear untapped upside as strength and shot continue to grow.'),
            (5, 'Kingston', 'Flemings', 'PG', '6-4', 190, 19, 'Houston', 'all_star', "Prospect Markelle Fultz, bigger De'Aaron Fox", 'Dynamic first step and paint pressure profile with all-NBA level athletic upside.'),
            (6, 'Mikel', 'Brown Jr.', 'PG', '6-5', 190, 19, 'Louisville', 'all_star', "Faster D'Angelo Russell", 'Explosive scoring guard who should benefit heavily from NBA spacing and pace.'),
            (7, 'Darius', 'Acuff Jr.', 'PG', '6-2', 190, 19, 'Arkansas', 'all_star', 'Damian Lillard style scoring profile', 'Dominant freshman-level production with elite handle, shot-making, and lead-guard orchestration.'),
            (8, 'Keaton', 'Wagler', 'SG', '6-6', 185, 19, 'Illinois', 'all_star', 'Positionless combo guard archetype', 'Silky pace/rhythm creator with multi-role offensive value despite average vertical pop.'),
            (9, 'Hannes', 'Steinbach', 'PF', '6-11', 248, 19, 'Washington', 'all_star', 'David Lee, Isaiah Hartenstein+', 'Motor, rebounding, transition impact, and improving floor-spacing profile pop on tape.'),
            (10, 'Braylon', 'Mullins', 'SG', '6-6', 205, 19, 'UConn', 'starter', 'High-end shooting wing archetype', 'Enigmatic but flashes all-star shotmaking; still trending upward after early injury return.'),
            (11, 'Brayden', 'Burries', 'SG', '6-4', 200, 19, 'Arizona', 'starter', 'Jared McCain', 'Stock has recovered with strong two-way starter indicators and better consistency.'),
            (12, 'Labaron', 'Philon', 'PG', '6-3', 175, 20, 'Alabama', 'starter', 'Tyrese Maxey lite', 'Smooth offensive operator and feisty defender with leadership traits at point guard.'),
            (13, 'Nate', 'Ament', 'SF', '6-10', 207, 19, 'Tennessee', 'starter', 'Keith Van Horn style outcome', 'Skilled tall wing projecting as a quality starter/role-player more than a true primary star.'),
            (14, 'Karim', 'Lopez', 'SF', '6-8', 215, 18, 'NZ Breakers (NBL)', 'starter', 'Tristan da Silva', 'Poised power wing prospect handling grown-pro competition with touch and feel.'),
            (15, 'Chris', 'Cenac Jr.', 'C', '6-10', 233, 19, 'Houston', 'starter', "Jaren Jackson Jr., Kel'el Ware", 'High-upside long big; development timeline may be longer but payoff can be major.'),
            (16, 'Yaxel', 'Lendeborg', 'PF', '6-9', 235, 22, 'Michigan', 'rotation', 'Kyle Kuzma, Obi Toppin+', 'Older but NBA-ready forward with broad contributions and stable roster-fit projection.'),
            (17, 'Amari', 'Allen', 'SF', '6-8', 215, 19, 'Alabama', 'rotation', 'Mature role-wing archetype', 'Efficient mature connector wing who plays a clean, winning role-player game.'),
            (18, 'Alijah', 'Arenas', 'SG', '6-6', 195, 19, 'USC', 'rotation', 'Upside project scoring guard', 'Small sample but clear NBA tools; longer-term project with significant upside if refined.'),
            (19, 'Dailyn', 'Swain', 'SF', '6-8', 220, 21, 'Texas', 'rotation', 'Herb Jones, Jeremy Grant', 'Elite athlete with developing offensive skill package and clear wing defender path.'),
            (20, 'Cameron', 'Carr', 'SG', '6-6', 185, 20, 'Baylor', 'rotation', 'Jaylon Tyson', 'Breakout 3-and-D style wing season with strong transition finishing and shooting profile.'),
        ]

        image_urls = {
            1: 'https://a.espncdn.com/combiner/i?img=/i/headshots/mens-college-basketball/players/full/5041955.png&w=350&h=254',
            2: 'https://a.espncdn.com/combiner/i?img=/i/headshots/mens-college-basketball/players/full/5142718.png&w=350&h=254',
            3: 'https://a.espncdn.com/combiner/i?img=/i/headshots/mens-college-basketball/players/full/5041935.png&w=350&h=254',
            4: 'https://a.espncdn.com/combiner/i?img=/i/headshots/mens-college-basketball/players/full/5095151.png&w=350&h=254',
            5: 'https://a.espncdn.com/combiner/i?img=/i/headshots/mens-college-basketball/players/full/5149077.png&w=350&h=254',
            6: 'https://a.espncdn.com/combiner/i?img=/i/headshots/mens-college-basketball/players/full/5101761.png&w=350&h=254',
            7: 'https://a.espncdn.com/combiner/i?img=/i/headshots/mens-college-basketball/players/full/5142620.png&w=350&h=254',
            8: 'https://a.espncdn.com/combiner/i?img=/i/headshots/mens-college-basketball/players/full/5254165.png&w=350&h=254',
            9: 'https://images.unsplash.com/photo-1571019613540-996a0f3b4f06',
            10: 'https://images.unsplash.com/photo-1547347298-4074fc3086f0',
            11: 'https://images.unsplash.com/photo-1485395037613-e83d5c1f5290',
            12: 'https://images.unsplash.com/photo-1517649763962-0c623066013b',
            13: 'https://images.unsplash.com/photo-1505666287802-931dc83a5dc7',
            14: 'https://images.unsplash.com/photo-1577223625816-7546f13df25d',
            15: 'https://images.unsplash.com/photo-1571019613576-2b22c76fd955',
            16: 'https://images.unsplash.com/photo-1526232761682-d26e03ac148e',
            17: 'https://images.unsplash.com/photo-1505664194779-8beaceb93744',
            18: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5',
            19: 'https://images.unsplash.com/photo-1495555961986-6d4c1ecb7be7',
            20: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b',
        }
        scout_users = [
            'alvinzhu',
            'jkim_scout',
            'maria_hoops',
            'devin_filmroom',
            'sam_data_model',
        ]

        for pick, first, last, pos, height, weight, age, school, level, comp, summary in board:
            player = Player.objects.create(
                first_name=first,
                last_name=last,
                position=pos,
                height=height,
                weight=weight,
                age=age,
                team=teams[school],
                projected_pick=pick,
                image_url=image_urls.get(pick, ''),
                bio=summary,
            )

            report = ScoutingReport.objects.create(
                player=player,
                contributor=scout_users[0],
                summary=summary,
                strengths='Scoring upside, offensive tools, and translatable role value.',
                weaknesses='Needs consistency growth and added polish in swing-skill areas.',
                nba_comparison=comp,
                projected_nba_level=level,
                is_locked=True,
            )

            base = 100 - pick
            SkillGrade.objects.create(
                report=report,
                shooting=max(70, min(96, base + 5)),
                finishing=max(68, min(95, base + 2)),
                playmaking=max(65, min(94, base + 1)),
                defense=max(64, min(93, base)),
                athleticism=max(66, min(95, base + 3)),
                rebounding=max(60, min(92, base - 1)),
                iq=max(70, min(95, base + 1)),
                overall_grade=max(74, min(96, base + 2)),
            )

            if pick <= 10:
                alt_level = 'all_star' if level == 'superstar' else level
                second_report = ScoutingReport.objects.create(
                    player=player,
                    contributor=scout_users[(pick % (len(scout_users) - 1)) + 1],
                    summary=f'Film-room take: {first} {last} has high-end translatable tools with upside tied to role clarity.',
                    strengths='Live-dribble creation, competitive drive, and situational versatility.',
                    weaknesses='Needs cleaner decision consistency versus elite size and pressure.',
                    nba_comparison=comp,
                    projected_nba_level=alt_level,
                    is_locked=True,
                )
                SkillGrade.objects.create(
                    report=second_report,
                    shooting=max(68, min(95, base + 3)),
                    finishing=max(67, min(94, base + 1)),
                    playmaking=max(64, min(93, base)),
                    defense=max(63, min(92, base - 1)),
                    athleticism=max(65, min(94, base + 2)),
                    rebounding=max(60, min(90, base - 2)),
                    iq=max(69, min(94, base)),
                    overall_grade=max(72, min(95, base + 1)),
                )

            if pick <= 5:
                third_report = ScoutingReport.objects.create(
                    player=player,
                    contributor='coach_tape_breakdown',
                    summary=f'Scheme fit view: {first} {last} profiles as a premium upside bet with strong two-way development path.',
                    strengths='Transition scoring, pressure creation, and growth-friendly toolset.',
                    weaknesses='Handle/counter depth and off-ball defensive consistency need refinement.',
                    nba_comparison=comp,
                    projected_nba_level='superstar' if pick <= 3 else 'all_star',
                    is_locked=True,
                )
                SkillGrade.objects.create(
                    report=third_report,
                    shooting=max(69, min(96, base + 4)),
                    finishing=max(68, min(95, base + 2)),
                    playmaking=max(65, min(94, base + 1)),
                    defense=max(64, min(93, base)),
                    athleticism=max(66, min(95, base + 3)),
                    rebounding=max(61, min(91, base - 1)),
                    iq=max(70, min(95, base + 1)),
                    overall_grade=max(73, min(96, base + 2)),
                )

        self.stdout.write(self.style.SUCCESS('Loaded top-20 board with multiple user scouting reports.'))
