import json
import math

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from py3dbp import Packer, Bin, Item

from .models import Palete


@method_decorator(csrf_exempt, name='dispatch')
class TetrisView(View):
    def post(self, request):
        box_mass = []
        bloc_mass = []
        unit_mass = []
        palete = Palete()

        f = open('test.json')

        post_body = json.load(f)

        f.close()

        palete.x = post_body["tara_length"]
        palete.y = post_body["tara_width"]
        palete.z = post_body["tara_height"]

        for item in post_body["productList"]:
            for i in item["productDimentions"]:
                i["name"] = item["productName"]
                if i["type"] == "кор":
                    count = 0
                    while count < i["quantity"]:
                        box_mass.append(i)
                        count += 1
                elif i["type"] == "бло":
                    count = 0
                    while count < i["quantity"]:
                        bloc_mass.append(i)
                        count += 1
                else:
                    count = 0
                    while count < i["quantity"]:
                        unit_mass.append(i)
                        count += 1

        all_type_mass = []
        for box in box_mass:
            all_type_mass.append(box)
        for bloc in bloc_mass:
            all_type_mass.append(bloc)
        for unit in unit_mass:
            all_type_mass.append(unit)

        bouble_sort(all_type_mass)

        packer = Packer()

        packer.add_bin(Bin('palete', palete.y, palete.x, palete.z, 999999))

        for i in all_type_mass:
            packer.add_item(Item(i["name"], i["width"], i["length"], i["height"], 0.1))

        packer.pack(True, False, 0)

        print("UNFITTED ITEMS:")
        for item in packer.bins[0].unfitted_items:
            print("====> ", item.string())

        for item in packer.bins[0].items:
            item.position = convert_to_int(item.position)


        json_response = to_json_response(packer.bins[0].items)

        return JsonResponse(json_response, safe=False)


def convert_to_int(items_in_bin):
    item_mass = [math.ceil(items_in_bin[0] / 10), math.ceil(items_in_bin[1] / 10), math.ceil(items_in_bin[2] / 10)]
    return item_mass


def to_json_response(to_json_data):
    json_mass = []

    for item in to_json_data:
        tmp = {
            "name": str(item.name),
            "scale_x": math.ceil(item.width / 10) + 0.0,
            "scale_y": math.ceil(item.height / 10) + 0.0,
            "scale_z": math.ceil(item.depth / 10) + 0.0,
            "position_x": item.position[1] + 0.0,
            "position_y": item.position[0] + 0.0,
            "position_z": item.position[2] + 0.0
        }
        json_mass.append(tmp)
    return json_mass


def bouble_sort(word):
    for item in word:
        for i in range(len(word) - 1):
            if word[i]["height"] < word[i + 1]["height"]:
                word[i]["height"], word[i + 1]["height"] = word[i + 1]["height"], word[i]["height"]
