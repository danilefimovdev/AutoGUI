from pynput.mouse import Button

MOUSE_BUTTONS = {
    'Button.left': Button.left,
    'Button.right': Button.right,
    'Button.middle': Button.middle,
}

LANGUAGES = {
    1024: "(no proofing)",
    1025: "Arabic (Saudi Arabia)",
    2049: "Arabic (Iraq)",
    3073: "Arabic (Egypt)",
    4097: "Arabic (Libya)",
    5121: "Arabic (Algeria)",
    6145: "Arabic (Morocco)",
    7169: "Arabic (Tunisia)",
    8193: "Arabic (Oman)",
    9217: "Arabic (Yemen)",
    10241: "Arabic (Syria)",
    11265: "Arabic (Jordan)",
    12289: "Arabic (Lebanon)",
    13313: "Arabic (Kuwait)",
    14337: "Arabic (U.A.E.)",
    15361: "Arabic (Bahrain)",
    16385: "Arabic (Qatar)",
    1026: "Bulgarian",
    1027: "Catalan",
    2051: "Valencian",
    1028: "Chinese (Taiwan)",
    2052: "Chinese (PRC)",
    307: "Chinese (Hong Kong SAR)",
    4100: "Chinese (Singapore)",
    5124: "Chinese (Macao SAR)",
    1029: "Czech",
    1030: "Danish",
    1031: "German (Germany)",
    2055: "German (Switzerland)",
    3079: "German (Austria)",
    4103: "German (Luxembourg)",
    5127: "German (Liechtenstein)",
    1032: "Greek",
    1033: "English (United States)",
    2057: "English (United Kingdom)",
    3081: "English (Australia)",
    4105: "English (Canada)",
    5129: "English (New Zealand)",
    6153: "English (Ireland)",
    7177: "English (South Africa)",
    8201: "English (Jamaica)",
    9225: "English (Caribbean)",
    10249: "English (Belize)",
    11273: "English (Trinidad and Tobago)",
    12297: "English (Zimbabwe)",
    13321: "English (Philippines)",
    14345: "English (Indonesia)",
    15369: "English (Hong Kong SAR)",
    16393: "English (India)",
    17417: "English (Malaysia)",
    18441: "English (Singapore)",
    1034: "Spanish (Spain, Traditional Sort)",
    2058: "Spanish (Mexico)",
    3082: "Spanish (Spain)",
    4106: "Spanish (Guatemala)",
    5130: "Spanish (Costa Rica)",
    6154: "Spanish (Panama)",
    7178: "Spanish (Dominican Republic)",
    8202: "Spanish (Venezuela)",
    9226: "Spanish (Colombia)",
    10250: "Spanish (Peru)",
    11274: "Spanish (Argentina)",
    12298: "Spanish (Ecuador)",
    13322: "Spanish (Chile)",
    14346: "Spanish (Uruguay)",
    15370: "Spanish (Paraguay)",
    16394: "Spanish (Bolivia)",
    17418: "Spanish (El Salvador)",
    18442: "Spanish (Honduras)",
    19466: "Spanish (Nicaragua)",
    20490: "Spanish (Puerto Rico)",
    21514: "Spanish (United States)",
    22538: "Spanish (Latin America)",
    1035: "Finnish",
    1036: "French (France)",
    2060: "French (Belgium)",
    3084: "French (Canada)",
    4108: "French (Switzerland)",
    5132: "French (Luxembourg)",
    6156: "French (Monaco)",
    7180: "French (Caribbean)",
    8204: "French (Reunion)",
    9228: "French (Congo (DRC)",
    10252: "French (Senegal)",
    11276: "French (Cameroon)",
    12300: "French (Côte d'Ivoire)",
    13324: "French (Mali)",
    14348: "French (Morocco)",
    15372: "French (Haiti)",
    1037: "Hebrew",
    1038: "Hungarian",
    1039: "Icelandic",
    1040: "Italian (Italy)",
    2064: "Italian (Switzerland)",
    1041: "Japanese",
    1042: "Korean",
    1043: "Dutch (Netherlands)",
    2067: "Dutch (Belgium)",
    1044: "Norwegian (Bokmål)",
    2068: "Norwegian (Nynorsk)",
    1045: "Polish",
    1046: "Portuguese (Brazil)",
    2070: "Portuguese (Portugal)",
    1047: "Romansh",
    1048: "Romanian",
    2072: "Romanian (Moldova)",
    1049: "Russian",
    2073: "Russian (Moldova)",
    1050: "Croatian (Croatia)",
    2074: "Serbian (Latin, Serbia and Montenegro (Former))",
    3098: "Serbian (Cyrillic, Serbia and Montenegro (Former))",
    4122: "Croatian (Bosnia and Herzegovina)",
    5146: "Bosnian (Latin)",
    6170: "Serbian (Latin, Bosnia and Herzegovina)",
    7194: "Serbian (Cyrillic, Bosnia and Herzegovina)",
    8218: "Bosnian (Cyrillic)",
    9242: "Serbian (Latin, Serbia)",
    10266: "Serbian (Cyrillic, Serbia)",
    11290: "Serbian (Latin, Montenegro)",
    12314: "Serbian (Cyrillic, Montenegro)",
    1051: "Slovak",
    1052: "Albanian",
    1053: "Swedish (Sweden)",
    2077: "Swedish (Finland)",
    1054: "Thai",
    1055: "Turkish",
    1056: "Urdu (Pakistan)",
    2080: "Urdu (India)",
    1057: "Indonesian",
    1058: "Ukrainian",
    1059: "Belarusian",
    1060: "Slovenian",
    1061: "Estonian",
    1062: "Latvian",
    1063: "Lithuanian",
    1064: "Tajik",
    1065: "Persian",
    1066: "Vietnamese",
    1067: "Armenian",
    1068: "Azerbaijani (Latin)",
    2092: "Azerbaijani (Cyrillic)",
    1069: "Basque",
    1070: "Upper Sorbian",
    2094: "Lower Sorbian",
    1071: "Macedonian",
    1072: "Sesotho (South Africa)",
    1073: "Xitsonga",
    1074: "Setswana (South Africa)",
    2098: "Setswana (Botswana)",
    1075: "Venda",
    1076: "isiXhosa",
    1077: "isiZulu",
    1078: "Afrikaans",
    1079: "Georgian",
    1080: "Faroese",
    1081: "Hindi",
    1082: "Maltese",
    1083: "Northern Sami (Norway)",
    2107: "Northern Sami (Sweden)",
    3131: "Northern Sami (Finland)",
    4155: "Lule Sami (Norway)",
    5179: "Lule Sami (Sweden)",
    6203: "Southern Sami (Norway)",
    7227: "Southern Sami (Sweden)",
    8251: "Skolt Sami (Finland)",
    9275: "Inari Sami (Finland)",
    2108: "Irish",
    1085: "Yiddish",
    1086: "Malay (Malaysia)",
    2110: "Malay (Brunei Darussalam)",
    1087: "Kazakh",
    1088: "Kyrgyz",
    1089: "Kiswahili",
    1090: "Turkmen",
    1091: "Uzbek (Latin)",
    2115: "Uzbek (Cyrillic)",
    1092: "Tatar",
    1093: "Bangla (India)",
    2117: "Bangla (Bangladesh)",
    1094: "Punjabi (India)",
    2118: "Punjabi (Pakistan)",
    1095: "Gujarati",
    1096: "Odia",
    1097: "Tamil (India)",
    2121: "amil (Sri Lanka)",
    1098: "Telugu",
    1099: "Kannada",
    1100: "Malayalam",
    1101: "Assamese",
    1102: "Marathi",
    1103: "Sanskrit",
    1104: "Mongolian (Cyrillic)",
    2128: "Mongolian (Traditional Mongolian, PRC)",
    3152: "Mongolian (Traditional Mongolian, Mongolia)",
    1105: "Tibetan (PRC)",
    1106: "Welsh",
    1107: "Khmer",
    1108: "Lao",
    1109: "Burmese",
    1110: "Galician",
    1111: "Konkani",
    1112: "Manipuri",
    1113: "Sindhi (Devanagari)",
    2137: "Sindhi (Arabic)",
    1114: "Syriac",
    1115: "Sinhala",
    1116: "Cherokee (Cherokee)",
    1117: "Inuktitut (Syllabics)",
    2141: "Inuktitut (Latin)",
    1118: "Amharic",
    1119: "Tamazight (Arabic, Morocco)",
    2143: "Tamazight (Latin, Algeria)",
    4191: "Tamazight (Tifinagh, Morocco)",
    1120: "Kashmiri (Arabic)",
    2144: "Kashmiri",
    1121: "Nepali",
    2145: "Nepali (India)",
    1122: "Frisian",
    1123: "Pashto",
    1124: "Filipino",
    1125: "Divehi",
    1126: "Edo",
    1127: "Fulah (Nigeria)",
    2151: "Fulah (Latin, Senegal)",
    1128: "Hausa",
    1129: "Ibibio (Nigeria)",
    1130: "Yoruba",
    1131: "Quechua (Bolivia)",
    2155: "Quechua (Ecuador)",
    3179: "Quechua (Peru)",
    1132: "Sesotho sa Leboa",
    1133: "Bashkir",
    1134: "Luxembourgish",
    1135: "Greenlandic",
    1136: "Igbo",
    1137: "Kanuri",
    1138: "Oromo",
    1139: "Tigrinya (Ethiopia)",
    2163: "Tigrinya (Eritrea)",
    1140: "Guaraní",
    1141: "Hawaiian",
    1142: "Latin",
    1143: "Somali",
    1144: "Yi (PRC)",
    1145: "Papiamentu",
    1146: "Mapudungun",
    1148: "Mohawk",
    1150: "Breton",
    1152: "Uyghur (PRC)",
    1153: "Maori",
    1154: "Occitan",
    1155: "Corsican",
    1156: "Alsatian",
    1157: "Sakha",
    1158: "K'iche'",
    1159: "Kinyarwanda",
    1160: "Wolof",
    1164: "Dari",
    1169: "Scottish Gaelic (United Kingdom)",
    1170: "Central Kurdish (Iraq)",
}