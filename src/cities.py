"""Modest database of more than a hundred world cities."""

import ephem
from StringIO import StringIO

_city_data = {
    'London': ('51.5', '-0.1166667', 14.935200),
    'Paris': ('48.8666667', '2.3333333', 34.747200),
    'New York': ('40.71417', '-74.00639', 1.828800),
    'Tokyo': ('35.685', '139.7513889', 17.983200),
    'Chicago': ('41.85', '-87.65', 177.698400),
    'Frankfurt': ('50.1166667', '8.6833333', 112.776000),
    'Hong Kong': ('22.2833333', '114.15', 88.696800),
    'Los Angeles': ('10.9322222', '-74.8627778', 41.757600),
    'Milan': ('45.4666667', '9.2', 102.717600),
    'Singapore': ('1.2930556', '103.8558333', 0.914400),
    'San Francisco': ('19.3333333', '-99.1166667', 2217.724800),
    'Sydney': ('-33.8833333', '151.2166667', 0.914400),
    'Toronto': ('43.6666667', '-79.4166667', 105.765600),
    'Zurich': ('47.3666667', '8.55', 433.730400),
    'Brussels': ('50.8333333', '4.3333333', 76.809600),
    'Madrid': ('40.4', '-3.6833333', 588.873600),
    'Mexico City': ('19.4', '-99.05', 2223.820800),
    'Sao Paulo': ('-23.5333333', '-46.6166667', 637.946400),
    'Moscow': ('55.7522222', '37.6155556', 124.968000),
    'Seoul': ('37.5663889', '126.9997222', 33.832800),
    'Amsterdam': ('52.35', '4.9166667', -1.828800),
    'Boston': ('42.35833', '-71.06028', 2.743200),
    'Caracas': ('10.5', '-66.9166667', 909.828000),
    'Dallas': ('32.78333', '-96.8', 137.769600),
    'Dusseldorf': ('51.2166667', '6.7666667', 39.928800),
    'Geneva': ('41.85722', '-71.44333', 28.956000),
    'Houston': ('29.76306', '-95.36306', 14.935200),
    'Jakarta': ('-6.1744444', '106.8294444', 3.962400),
    'Johannesburg': ('-26.2', '28.0833333', 1765.706400),
    'Melbourne': ('-37.8166667', '144.9666667', 63.703200),
    'Osaka': ('34.6666667', '135.5', 4.876800),
    'Prague': ('50.0833333', '14.4666667', 244.754400),
    'Santiago': ('-33.45', '-70.6666667', 521.817600),
    'Taipei': ('25.0166667', '121.45', 5.791200),
    'Washington': ('38.895', '-77.03667', 2.743200),
    'Bangkok': ('13.75', '100.5166667', 1.828800),
    'Beijing': ('39.9288889', '116.3883333', 63.703200),
    'Montreal': ('45.5', '-73.5833333', 52.730400),
    'Rome': ('41.9', '12.4833333', 14.935200),
    'Stockholm': ('59.3333333', '18.05', 15.849600),
    'Warsaw': ('41.43972', '-75.61639', 302.971200),
    'Atlanta': ('33.74889', '-84.38806', 304.800000),
    'Barcelona': ('41.3833333', '2.1833333', 0.914400),
    'Berlin': ('6.2833333', '-75.5666667', 1576.730400),
    'Buenos Aires': ('10.4833333', '-66.9166667', 916.838400),
    'Budapest': ('47.5', '19.0833333', 102.717600),
    'Copenhagen': ('55.6666667', '12.5833333', 0.914400),
    'Hamburg': ('53.55', '10', 2.743200),
    'Istanbul': ('41.0186111', '28.9647222', 23.774400),
    'Kuala Lumpur': ('3.1666667', '101.7', 60.960000),
    'Manila': ('14.6041667', '120.9822222', 7.924800),
    'Miami': ('25.77389', '-80.19389', 0.914400),
    'Minneapolis': ('44.98', '-93.26361', 258.775200),
    'Munich': ('48.15', '11.5833333', 508.711200),
    'Shanghai': ('31.2222222', '121.4580556', 7.924800),
    'Athens': ('33.92', '-118.28028', 34.747200),
    'Auckland': ('-36.8666667', '174.7666667', 25.908000),
    'Dublin': ('53.3330556', '-6.2488889', 8.839200),
    'Helsinki': ('60.1755556', '24.9341667', 25.908000),
    'Luxembourg': ('49.6116667', '6.13', 273.710400),
    'Lyon': ('45.75', '4.85', 174.955200),
    'Mumbai': ('18.975', '72.8258333', 27.736800),
    'New Delhi': ('28.6', '77.2', 210.921600),
    'Philadelphia': ('39.95222', '-75.16417', 2.743200),
    'Rio de Janeiro': ('-22.9', '-43.2333333', 10.972800),
    'Tel Aviv': ('32.0666667', '34.7666667', 34.747200),
    'Vienna': ('48.2', '16.3666667', 170.992800),
    'Abu Dhabi': ('24.4666667', '54.3666667', 13.716000),
    'Almaty': ('43.25', '76.95', 861.974400),
    'Birmingham': ('52.4666667', '-1.9166667', 133.807200),
    'Bogota': ('4.6', '-74.0833333', 2619.756000),
    'Bratislava': ('48.15', '17.1166667', 131.978400),
    'Brisbane': ('-27.5', '153.0166667', 24.993600),
    'Bucharest': ('44.4333333', '26.1', 70.713600),
    'Cairo': ('30.05', '31.25', 22.860000),
    'Cleveland': ('41.49944', '-81.69556', 195.986400),
    'Cologne': ('50.9333333', '6.95', 45.720000),
    'Detroit': ('42.33139', '-83.04583', 173.736000),
    'Dubai': ('27.65', '78.2833333', 176.784000),
    'Ho Chi Minh City': ('10.75', '106.6666667', 3.962400),
    'Kiev': ('50.4333333', '30.5166667', 168.859200),
    'Lima': ('-12.05', '-77.05', 107.899200),
    'Lisbon': ('38.7166667', '-9.1333333', 15.849600),
    'Manchester': ('53.5', '-2.2166667', 72.847200),
    'Montevideo': ('-34.8580556', '-56.1708333', 43.891200),
    'Oslo': ('59.9166667', '10.75', 12.801600),
    'Rotterdam': ('51.9166667', '4.5', -2.743200),
    'Riyadh': ('35.3', '43.9166667', 196.900800),
    'Seattle': ('47.60639', '-122.33083', 59.740800),
    'Stuttgart': ('48.7666667', '9.1833333', 414.832800),
    'The Hague': ('52.0833333', '4.3', 1.828800),
    'Vancouver': ('49.25', '-123.1333333', 71.932800),
    'Adelaide': ('-34.9333333', '138.6', 71.932800),
    'Antwerp': ('51.2166667', '4.4166667', 3.962400),
    'Arhus': ('56.15', '10.2166667', 0.914400),
    'Baltimore': ('39.29028', '-76.6125', 1.828800),
    'Bangalore': ('12.9833333', '77.5833333', 913.790400),
    'Bologna': ('44.4833333', '11.3333333', 101.803200),
    'Brazilia': ('-16.2119444', '-44.4308333', 811.987200),
    'Calgary': ('51.0833333', '-114.0833333', 1087.831200),
    'Cape Town': ('-33.9166667', '18.4166667', 6.705600),
    'Colombo': ('6.9319444', '79.8477778', 4.876800),
    'Columbus': ('39.96111', '-82.99889', 234.696000),
    'Dresden': ('51.05', '13.75', 110.947200),
    'Edinburgh': ('55.95', '-3.2', 31.699200),
    'Genoa': ('29.62306', '-95.19694', 12.801600),
    'Glasgow': ('55.8333333', '-4.25', 65.836800),
    'Gothenburg': ('57.7166667', '11.9666667', 4.876800),
    'Guangzhou': ('23.1166667', '113.25', 0.914400),
    'Hanoi': ('21.0333333', '105.85', 25.908000),
    'Kansas City': ('39.09972', '-94.57833', 267.919200),
    'Leeds': ('39.05583', '-94.50833', 232.867200),
    'Lille': ('50.6333333', '3.0666667', 24.993600),
    'Marseille': ('43.3', '5.4', 53.949600),
    'Richmond': ('39.99333', '-75.10056', 6.705600),
    'St. Petersburg': ('59.8944444', '30.2641667', 4.876800),
    'Tashkent': ('41.3166667', '69.25', 459.943200),
    'Tehran': ('35.6719444', '51.4244444', 1138.732800),
    'Tijuana': ('32.5333333', '-117.0166667', 37.795200),
    'Turin': ('13.9663889', '-89.7661111', 649.833600),
    'Utrecht': ('52.0833333', '5.1333333', 0.914400),
    'Wellington': ('42.41111', '-71.08333', 0.914400),
    }

def city(name):
    try:
        data = _city_data[name]
    except KeyError:
        raise KeyError('Unknown city: %r' % (name,))
    o = ephem.Observer()
    o.name = name
    o.lat, o.long, o.elevation = data
    return o
