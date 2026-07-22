from django.core.management.base import BaseCommand
from django.db import transaction
from prediction.models import Shehia, Bin

MAPPING = {
    "Amani":["AmaniA","AmaniB","AmaniC","AmaniD"],
    "Banko":["BankoA","BankoB","BankoC","BankoD"],
    "Chumbuni":["ChumbuniA","ChumbuniB","ChumbuniC","ChumbuniD","ChumbuniE"],
    "Gulioni":["GulioniA","GulioniB","GulioniC"],
    "Jangombe":["JangombeA","JangombeB","JangombeC","JangombeD","JangombeE"],
    "Karakana":["KarakanaA","KarakanaB","KarakanaC"],
    "Kidongo Chekundu":["KidongoA","KidongoB"],
    "Kikwajuni Bondeni":["KikwajuniA","KikwajuniB","KikwajuniC"],
    "Kikwajuni Juu":["KikwajuniJuuA","KikwajuniJuuB","KikwajuniJuuC"],
    "Kilimahewa Bondeni":["Kilima_bondeniA","Kilima_bondeniB","Kilima_bondeniC","Kilima_bondeniD","Kilima_bondeniE"],
    "Kilimahewa Juu":["Kilima_juuA","Kilima_juuB","Kilima_juuC","Kilima_juuD"],
    "Kilimani":["KilimaniA","KilimaniB","KilimaniC"],
    "Kiponda":["KipondaA","KipondaB","KipondaC"],
    "Kisima Majongoo":["KisimaA","KisimaB","KisimaC"],
    "Kisiwandui":["KisiwaA","KisiwaB","KisiwaC"],
    "Kwaalimsha":["KwaalimshaA","KwaalimshaB","KwaalimshaC"],
    "Kwaalinatu":["KwaliNatuA","KwaliNatuB","KwaliNatuC"],
    "Kwabintiamrani":["KwabintiamranA","KwabintiamranB","KwabintiamranC","KwabintiamranD"],
    "Kwahani":["KwahaniA","KwahaniB","KwahaniC"],
    "Kwamtipura":["KwamtipuraA","KwamtipuraB","KwamtipuraC","KwamtipuraD","KwamtipuraE"],
    "Kwamtumwajeni":["KwamtumwajeniA","KwamtumwajeniB","KwamtumwajeniC"],
    "Kwa Wazee":["WazeeA","WazeeB","WazeeC","WazeeD"],
    "Magomeni":["MagomeniA","MagomeniB","MagomeniC","MagomeniD","MagomeniE","MagomeniF"],
    "Makadara":["MakadaraA","MakadaraB","MakadaraC"],
    "Malindi":["MalindiA","MalindiB","MalindiC"],
    "Mapinduzi":["MapinduziA","MapinduziB"],
    "Maruhubi":["MaruhubiA","MaruhubiB","MaruhubiC","MaruhubiD"],
    "Masumbani":["MasumbaniA","MasumbaniB","MasumbaniC","MasumbaniD"],
    "Matarumbeta":["MatarumbetaA","MatarumbetaB","MatarumbetaC","MatarumbetaD"],
    "Mboriborini":["MboriA","MboriB","MboriC","MboriD"],
    "Mchangani":["MchanganiA","MchanganiB","MchanganiC"],
    "Meya":["MeyaA","MeyaB","MeyaC","MeyaD"],
    "Miembeni":["MiembeniA","MiembeniB","MiembeniC","MiembeniD"],
    "Migombani":["MigombaniA","MigombaniB","Migombani","MigombaniD","MigombaniE"],
    "Mikunguni":["MikunguniA","MikunguniB","MikunguniC"],
    "Mitiulaya":["MitiA","MitiB","MitiC"],
    "Mkele":["MkeleA","MkeleB","MkeleC"],
    "Mkunazini":["MkunaziniA","MkunaziniB"],
    "Mlandege":["MlandegeA","MlandegeB"],
    "Mnazimmoja":["MnazimmojaA","MnazimmojaB"],
    "Mpendae":["MpendaeA","MpendaeB","MpendaeC","MpendaeD"],
    "Muungano":["MuunganoA","MuunganoB","MuunganoC","MuunganoD"],
    "Mwembeladu":["MwembeladuA","MwembeladuB","MwembeladuC"],
    "MwembeMadema":["MwembeMademaA","MwembeMademaB"],
    "Mwembe Makumbi":["MwembeMakumbiA","Mwembe MakumbiB","MwembeMakumbiC","MwembeMakumbiD"],
    "Mwembeshauri (Muembeshauri)": ["MuembeshauriA","MuembeshauriB"],
    "Mwembetanga (Muembetanga)": ["MuembetangaA","MuembetangaB"],
    "Nyerere":["NyerereA","NyerereB","NyerereC","NyerereD"],
    "Rahaleo":["RahaleoeA","RahaleoB","RahaleoC"],
    "Saateni":["SaateniA","SaateniB","SaateniC"],
    "Sebleni":["SebleniA","SebleniB","SebleniC","SebleniD"],
    "Shangani":["ShanganiA","ShanganiB"],
    "Shaurimoyo":["ShaurimoyoA","Shaurimoyo","Shaurimoyo","ShaurimoyoD"],
    "Sogea":["SogeaA","SogeaB","SogeaC","SogeaD"],
    "Urusi":["UrusiA","UrusiB","UrusiC","UrusiD"],
    "Vikokotoni":["VikokotoniA","VikokotoniB"],
}

class Command(BaseCommand):
    help = 'Populate Shehia and Bin records from predefined mapping'

    def handle(self, *args, **options):
        created_shehias = 0
        created_bins = 0
        with transaction.atomic():
            for shehia_name, bins in MAPPING.items():
                shehia_obj, shehia_created = Shehia.objects.get_or_create(name=shehia_name)
                if shehia_created:
                    created_shehias += 1
                for bin_name in bins:
                    bin_obj, bin_created = Bin.objects.get_or_create(shehia=shehia_obj, name=bin_name)
                    if bin_created:
                        created_bins += 1
        self.stdout.write(self.style.SUCCESS(f'Created/verified {created_shehias} Shehias and {created_bins} Bins.'))
