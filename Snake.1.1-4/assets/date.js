class GenerateDate {
   constructor(selector, mathDay) {
      this.$el = document.querySelectorAll(selector);
      this.day = mathDay;
   }

   getDate() {
      const DAY = 86400000;
      const full = new Date(Date.now() + this.day * DAY);
      const year = full.getFullYear();
      const date = String(full.getDate()).padStart(2, "0");
      const month = String(full.getMonth() + 1).padStart(2, "0");
      this.render(`${date}.${month}.${year}`);
   }

   getMonth(countyCode) {
      const CODE = {
         // Russian
         ru: ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"],
         // Ukrainian
         ua: ["січень", "лютий", "березень", "квітень", "травень", "червень", "липень", "серпень", "вересень", "жовтень", "листопад", "грудень"],
         // Greek
         gr: ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"],
         // English
         en: ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"],
         // Georgian
         ge: ["იანვარი", "თებერვალი", "მარში", "აპრილი", "მაისი", "ივნისი", "ივლისი", "აგვისტო", "სექტემბერი", "ოქტომბერი", "ნოემბერი", "დეკემბერი"],
         // Azerbaijani
         az: ["yanvar", "fevral", "mart", "aprel", "bilər", "iyun", "iyul", "avqust", "sentyabr", "oktyabr", "noyabr", "dekabr"],
         // Turkish
         tr: ["ocak", "subat", "mart", "nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım", "aralık"],
         // Polish
         pl: ["styczeń", "luty", "marsz", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"],
         // Spanish
         es: ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
         //Potugal
         pt: ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
         // Romanian
         ro: ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"],
         // Italian
         it: ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"],
         // Macedonian
         md: ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"],
         // Kazakh
         kz: ["қаңтар", "ақпан", "наурыз", "cәуір", "мамыр", "маусым", "шілде", "тамыз", "қыркүйек", "қазан", "қараша", "желтоқсан"],
         // Armenian
         am: ["հունվար", "փետրվар", "մարտ", "ապրիլ", "մայիս", "հունիս", "հուլիս", "օգոստոս", "սեպտեմբեր", "հոկտեմբեր", "նոյեմբեր", "դեկտեմբեր"],
         // Serbian
         sr: ["januara", "februara", "marta", "april", "može", "juna", "jul", "avgusta", "septembar", "oktobar", "novembar", "decembar"],
         // Albanian
         sq: ["janar", "shkurt", "marsh", "prill", "mund", "qershor", "korrik", "gusht", "shtator", "tetor", "nentor", "dhjetor"],
         // Arabic
         ar: ["يناير", "فبراير ", "مارس ", "أبريل ", "مايو ", "يونيو ", "يوليو ", "أغسطس ", "سبتمبر ", "أكتوبر ", "نوفمبر ", "ديسمبر "],
         // Slovenian
         sk: ["januára", "februára", "marca", "apríla", "smieť", "júna", "júla", "augusta", "septembra", "októbra", "november", "december"],
         // Bengali
         bn: ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"],
         // Bulgarian
         bg: ["януари", "февруари", "март", "април", "май", "юни", "юли", "август", "септември", "октомври", "ноември", "декември"],
         // Hungarian
         hu: ["január", "február", "március", "április", "május", "június", "július", "augusztus", "szeptember", "október", "november", "december"],
         // Czech
         cz: ["leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen", "září", "říjen", "listopad", "prosinec"],
         // Indonesian
         id: ["januari", "februari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november", "desember"],
         // Thai
         th: ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"],
         // French
         fr: ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
         // German
         de: ["januar", "februar", "märz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"],
         // Bosnian
         bs: ["јануар", "фебруар", "март", "април", "мај", "јуни", "јули", "аугуст", "септембар", "октобар", "новембар", "децембар"],
         // Lithuanian
         lt: ["sausis", "vasaris", "kovas", "balandis", "gegužė", "birželis", "liepa", "rugpjūtis", "rugsėjis", "spalis", "lapkritis", "gruodis"],
         // Uzbeck
         uz: ["январ", "феврал", "март", "апрел", "май", "июн", "июл", "август", "сентябр", "октябр", "ноябр", "декабр"],
         // Malay
         ms: ["januari", "februari", "mac", "april", "mei", "jun", "julai", "ogos", "september", "oktober", "november", "disember"],
      };
      const monthNumber = new Date().getMonth() + 1 + this.day;
      const monthIndex = (monthNumber - 1) % 12;
      const monthText = CODE[countyCode][monthIndex].toLowerCase().trim();
      this.render(monthText);
   }

   getSeason(countyCode) {
      const SEASONS = {
         // Russian
         ru: ["зима", "весна", "лето", "осень"],
         // Ukrainian
         ua: ["зима", "весна", "літо", "осінь"],
         // Greek
         gr: ["χειμώνας", "άνοιξη", "καλοκαίρι", "φθινόπωρο"],
         // English
         en: ["winter", "spring", "summer", "fall"],
         // Georgian
         ge: ["ზამთარი", "გაზაფხული", "ზაფხული", "შემოდგომა"],
         // Azerbaijani
         az: ["qış", "yaz", "yay", "payız"],
         // Turkish
         tr: ["kış", "ilkbahar", "yaz", "sonbahar"],
         // Polish
         pl: ["zima", "wiosna", "lato", "jesień"],
         // Spanish
         es: ["invierno", "primavera", "verano", "otoño"],
         // Portuguese
         pt: ["inverno", "primavera", "verão", "outono"],
         // Romanian
         ro: ["iarna", "primăvara", "vara", "toamna"],
         // Italian
         it: ["inverno", "primavera", "estate", "autunno"],
         // Macedonian
         md: ["зима", "пролет", "лето", "есен"],
         // Kazakh
         kz: ["қыс", "көктем", "жаз", "күз"],
         // Armenian
         am: ["ձմեռ", "գարուն", "ամառ", "աշուն"],
         // Serbian
         sr: ["zima", "proleće", "leto", "jesen"],
         // Albanian
         sq: ["dimër", "pranverë", "verë", "vjeshtë"],
         // Arabic
         ar: ["الشتاء", "الربيع", "الصيف", "الخريف"],
         // Slovenian
         sk: ["zima", "pomlad", "poletje", "jesen"],
         // Bengali
         bn: ["শীতকাল", "বসন্ত", "গ্রীষ্মকাল", "শরৎ"],
         // Bulgarian
         bg: ["зима", "пролет", "лято", "есен"],
         // Hungarian
         hu: ["tél", "tavasz", "nyár", "ősz"],
         // Czech
         cz: ["zima", "jaro", "léto", "podzim"],
         // Indonesian
         id: ["musim dingin", "musim semi", "musim panas", "musim gugur"],
         // Thai
         th: ["ฤดูหนาว", "ฤดูใบไม้ผลิ", "ฤดูร้อน", "ฤดูใบไม้ร่วง"],
         // French
         fr: ["hiver", "printemps", "été", "automne"],
         // German
         de: ["winter", "frühling", "sommer", "herbst"],
         // Bosnian
         bs: ["zima", "proljeće", "ljeto", "jesen"],
         // Lithuanian
         lt: ["žiema", "pavasaris", "vasara", "ruduo"],
         // Uzbek
         uz: ["qish", "bahor", "yoz", "kuz"],
         // Malay
         ms: ["musim sejuk", "musim bunga", "musim panas", "musim luruh"],
      };

      const currentMonth = new Date().getMonth() + 1 + this.day;
      let seasonIndex;

      if ([12, 1, 2].includes(currentMonth)) {
         seasonIndex = 0; // Winter
      } else if ([3, 4, 5].includes(currentMonth)) {
         seasonIndex = 1; // Spring
      } else if ([6, 7, 8].includes(currentMonth)) {
         seasonIndex = 2; // Summer
      } else {
         seasonIndex = 3; // Fall
      }

      const seasonText = SEASONS[countyCode][seasonIndex];
      this.render(seasonText);
   }

   render(data) {
      this.$el.forEach((element) => {
         element.innerText = data;
      });
   }
}
