import pickle
import csv
import re

number_string_dict={
        "یک" : 1,
        "دو" : 2,
        "سه" : 3,
        "چهار" : 4,
        "پنج" : 5,
        "شیش" : 6,
        "شش" : 6,
        "هفت" : 7,
        "هشت" : 8,
        "نه" : 9,

}


def find_number(sr):
    output = ''
    for item in sr:
        if item.isdigit() or item == '.':
            output = output + item

    return float(output)


mobiles_dict_list = []
with open('all_mobiles_properties.pkl', 'rb') as f:
        mobiles_dict_list = pickle.load(f)

def length_width_height(di_size):
        di_size = di_size.replace("میلی\u200cمتر", " ")
        di_size = di_size.split("x") if "x" in di_size else di_size.split("×") if "×" in di_size else ""
        di_size = [float(x) for x in di_size]
        di_size.sort()
        if di_size[0] >= 40:
                di_size[0] = di_size[0] / 10
        return di_size[0], di_size[1], di_size[2]

def weight(weight_string):
        weight_string = weight_string.replace("گرم", "")
        weight_string = weight_string.replace("\u200d", "")
        return float(weight_string)

def size(size_string):
        return float(size_string.replace("اینچ", ""))

def pixels(pixels_string):
        return [int(m) for m in pixels_string.split() if m.isdigit()][0]

def number_of_camera(camera_string):
        if "بدون" in camera_string:
                return 0
        return [int(m) for m in camera_string.split() if m.isdigit()][0]

def resolution(resolution_string):
        if "qvga" in resolution_string.lower():
                return 0.08
        if "vga" in resolution_string.lower():
                return 0.3
        try:
                return [int(m) for m in resolution_string.split() if m.isdigit()][0]
        except:
                return 20
def internal_memory(internal_memory_string):
        if internal_memory_string == "یک ترابایت":
                return 1000
        if "مگابایت" in internal_memory_string:
                for key in number_string_dict.keys():
                        if key in internal_memory_string:
                                return number_string_dict[key] / 1000
        if "گیگابایت" in internal_memory_string:
                for key in number_string_dict.keys():
                        if key in internal_memory_string:
                                return number_string_dict[key]
        return [int(m) for m in internal_memory_string.split() if m.isdigit()][0]


def ram(ram_string):
        if "مگابایت" in ram_string:
                for key in number_string_dict.keys():
                        if key in ram_string:
                                return number_string_dict[key] / 1000
        if "گیگابایت" in ram_string:
                for value in number_string_dict.values():
                        if str(value) in ram_string:
                                return number_string_dict[key]
                for key in number_string_dict.keys():
                        if key in ram_string:
                                return number_string_dict[key]
        if "۱۲ گیگابایت" in ram_string:
                return 12
        if "۱۶ مگابایت" in ram_string:
                return 16/1000
        if "۲۴ مگابایت" in ram_string:
                return 24/1000
        if "۳۲ مگابایت" in ram_string:
                return 32/1000
        if "۶۴ مگابایت" in ram_string:
                return 64/1000
        if "۲۵۶ مگابایت" in ram_string:
                return 254/1000
        if "بدون حافظه RAM" in ram_string:
                return 0
        
def number_of_cores(entry):
    
    sum = 0

    last_char = ' '
    for char in entry:
        if char in 'xX' and last_char.isdigit():
            sum += int(last_char)
        if char == '(':
            break
        last_char = char

    for word in entry.split(' '):
        if word in ['Single-Core', 'Single-core', 'Single', 'single']:
            sum += 1
        elif word in ['Dual-Core', 'Dual-core', 'Dual', 'dual']:
            sum += 2
        elif word in ['Triple-Core', 'Triple-core', 'Triple', 'triple']:
            sum += 3
        elif word in ['Quad-Core', 'Quad-core', 'Quad', 'quad']:
            sum += 4
        elif word in ['Hexa-Core', 'Hexa-core', 'Hexa', 'hexa']:
            sum += 6
        elif word in ['Octa-Core', 'Octa-core', 'Octa', 'octa']:
            sum += 8

    return max(min(sum, 8), 1)


def clean_battery_attribute(attribute: str):
    mil_amper = 0
    wat = 0
    if ('ظرفیت' in attribute) and ('میلی‌آمپر' in attribute):
        mil_amper = int(attribute[attribute.index('ظرفیت') + len('ظرفیت'):attribute.index('میلی‌آمپر')])

    if ('وات') in attribute:
        wats = [m.start() for m in re.finditer('وات', attribute)]
        for item in wats:
            temp = find_number(attribute[(item - 4):item])
            if temp > wat:
                wat = temp

    return mil_amper, wat

all_mobiles_feature = []

for mobile_dict in mobiles_dict_list:
        feature_dict = {"length": 0, "width": 0, "height": 0,
                        "weight": 0, 
                        "size": 0,
                        "pixels": 0, 
                        "apple_chip" : 0, "Mediatek-chip": 0, "Exynos-chip": 0, 
                        "Snapdragon-chip": 0, "Unisoc-chip":0, "other-chip":0 ,
                        "number_of_cores": 0,
                        "apple-gpu": 0, "Adreno-gpu":0, "mali-gpu":0,
                        "PowerVR-gpu":0, "IMG-gpu": 0, "other-gpu":0, 
                        "internal_memory":0,
                        "ram":0,
                        "5g":0,
                        "module-no":0,
                        "image-resolution":0,
                        "ios":0,
                        "battery":0,
                        "battery-wat":0,
                        "price":0
                        }
        feature_dict['height'],feature_dict['width'], feature_dict['length'] = length_width_height(mobile_dict["ابعاد"])
        feature_dict['weight'] = weight(mobile_dict["وزن"])
        feature_dict['size'] = size(mobile_dict["اندازه"]) if "اندازه" in mobile_dict else 5.5
        feature_dict['pixels'] = pixels(mobile_dict["تراکم پیکسلی"]) if "تراکم پیکسلی" in mobile_dict else 300
        if "تراشه" in mobile_dict:
                feature_dict['apple_chip'] = 1 if "apple" in mobile_dict["تراشه"].lower() else 0
                feature_dict['Mediatek-chip'] = 1 if "mediatek" in mobile_dict["تراشه"].lower() or "mt" in mobile_dict["تراشه"].lower() else 0
                feature_dict['Snapdragon-chip'] = 1 if "snapdragon" in mobile_dict["تراشه"].lower() or "qualcomm" in mobile_dict["تراشه"].lower() else 0
                feature_dict['Unisoc-chip'] = 1 if "unisoc" in mobile_dict["تراشه"].lower() or "sc" in mobile_dict["تراشه"].lower() else 0
                # feature_dict['Kirin-chip'] = 1 if "kirin" in mobile_dict["تراشه"].lower() else 0
                feature_dict['Exynos-chip'] = 1 if "exynos" in mobile_dict["تراشه"].lower() else 0
        else:
                feature_dict['other-chip'] = 1
        
        feature_dict['number_of_cores'] = number_of_cores(mobile_dict['پردازنده\u200cی مرکزی']) if "پردازنده\u200cی مرکزی" in mobile_dict else 1
        
        if "پردازنده‌ی گرافیکی" in mobile_dict:
                feature_dict['apple-gpu'] = 1 if "apple" in mobile_dict["پردازنده‌ی گرافیکی"].lower() else 0
                feature_dict['Adreno-gpu'] = 1 if "adreno" in mobile_dict["پردازنده‌ی گرافیکی"].lower() else 0
                feature_dict['mali-gpu'] = 1 if "mali" in mobile_dict["پردازنده‌ی گرافیکی"].lower() else 0
                feature_dict['PowerVR-gpu'] = 1 if "powervr" in mobile_dict["پردازنده‌ی گرافیکی"].lower() else 0
                feature_dict['IMG-gpu'] = 1 if "img" in mobile_dict["پردازنده‌ی گرافیکی"].lower() else 0
        else:
                feature_dict['other-gpu'] = 1
        feature_dict['internal_memory'] = internal_memory(mobile_dict["حافظه داخلی"]) if "حافظه داخلی" in mobile_dict else 117
        feature_dict['ram'] = ram(mobile_dict['مقدار RAM']) if 'مقدار RAM' in mobile_dict else 5
        feature_dict['5g'] = 1 if "شبکه 5G" in mobile_dict else 0
        feature_dict['module-no'] = number_of_camera(mobile_dict['دوربین‌های پشت گوشی']) if "دوربین‌های پشت گوشی" in mobile_dict else 0
        feature_dict['image-resolution'] = resolution(mobile_dict['رزولوشن عکس']) if "رزولوشن عکس" in mobile_dict else 0
        feature_dict['ios'] = 1 if 'سیستم عامل' in mobile_dict and 'ios' in mobile_dict['سیستم عامل'].lower() else 0
        if "مشخصات باتری" in mobile_dict:
                feature_dict['battery'], feature_dict['battery-wat'] = clean_battery_attribute(mobile_dict['مشخصات باتری']) 
                if feature_dict['battery'] == 0:
                        feature_dict['battery'] = 3220
                if feature_dict['battery-wat'] == 0:
                        feature_dict['battery-wat'] = 20
        else:
                feature_dict['battery'], feature_dict['battery-wat'] = 3220, 20
        feature_dict["price"] = int(mobile_dict['price'].replace(",", ""))
        all_mobiles_feature.append(feature_dict)

size_sum, battery_sum, battery_wat_sum, ram_sum, pixel_sum, internal_memory_sum = 0, 0, 0, 0, 0, 0

# for mobile_feature in all_mobiles_feature:
#         size_sum += mobile_feature['size']
#         battery_sum += mobile_feature['battery']
#         battery_wat_sum += mobile_feature['battery-wat']
#         ram_sum += mobile_feature['ram']
#         pixel_sum += mobile_feature['pixels']
#         internal_memory_sum += mobile_feature['internal_memory']
# print ("size", size_sum/326) # 5.4916257668711665
# print ("size", battery_sum/326) #3218.665644171779
# print ("size", battery_wat_sum/326) #20.33282208588957
# print ("size", ram_sum/326) #4.870680981595089
# print ("size", pixel_sum/326) #299.37116564417175
# print ("size", internal_memory_sum/326) #116.8835858895706

# print(all_mobiles_feature)

with open("features_with_mean.csv", 'w',newline='') as csvfile:
        columns = list(all_mobiles_feature[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for key in all_mobiles_feature:
                writer.writerow(key)
