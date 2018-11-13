"""
Fuzzy Control System

Calculates insurance price per month based on BMI index, 
blood pressure, cholesterol level and cigarette consumption.

insurance.py <bmi_index> <blood_pressure> <cholestrerol_level> <cigarettes_per_day>
"""

import math
import sys

# Membership functions


def inc_mf(a, b, x):
    return max(min((x - a) / (b - a), 1), 0)


def dec_mf(a, b, x):
    return max(min((x - b) / (a - b), 1), 0)


def trap_mf(a, b, c, d, x):
    return max(min((x - a) / (b - a), 1, (d - x) / (d - c)), 0)


def tri_mf(a, b, c, d, x):
    return max(min((x - a) / (b - a), (c - x) / (c - b)), 0)


# BMI index
bmi = {'healthy': lambda x: trap_mf(16, 18.5, 25, 27.5, x),
       'unhealthy': lambda x: max(inc_mf(25, 30, x), dec_mf(16, 18.5, x))}

# blood pressume in mmHg
blp = {'low': lambda x: dec_mf(80, 140, x),
       'high': lambda x: inc_mf(120, 150, x)}

# cholesterol level in mg/dL
cho = {'low': lambda x: dec_mf(200, 240, x),
       'high': lambda x: inc_mf(230, 270, x)}

# cigarettes/day
cig = {'smoker': lambda x: 1 if x > 0 else 0,
       'non-smoker': lambda x: 1 if x <= 0 else 0}

# Rules
rules = [
    {
        # if BMI = unhealthy and blood pressure = HIGH and cholesterol = HIGH and smoker = TRUE
        'rule': lambda bm, bp, ch, cg: min(bmi['unhealthy'](bm), blp['high'](bp), cho['high'](ch), cig['smoker'](cg)),
        'res': lambda bm, bp, ch, cg: 40 + math.log(bm + bp + ch + cg)
    }, {
        # if BMI = unhealthy and either cholesterol = HIGH or blood pressure = HIGH
        'rule': lambda bm, bp, ch, cg: max(bmi['unhealthy'](bm), min(cho['high'](ch), blp['high'](bp))),
        'res': lambda bm, bp, ch, cg: 20 + 20 * math.log(bm)
    }, {
        # if blood pressure = HIGH and either BMI = unhealthy or cholesterol = HIGH
        'rule': lambda bm, bp, ch, cg: max(blp['high'](bp), min(bmi['unhealthy'](bm), cho['high'](ch))),
        'res': lambda bm, bp, ch, cg: 20 + 4 * math.log(bp)
    }, {
        # if cholesterol = HIGH and either BMI = unhealthy or blood pressure = HIGH
        'rule': lambda bm, bp, ch, cg: max(cho['high'](ch), min(bmi['unhealthy'](bm), blp['high'](bp))),
        'res': lambda bm, bp, ch, cg: 20 + 4 * math.log(ch)
    }, {
        # if smoker = TRUE
        'rule': lambda bm, bp, ch, cg: cig['smoker'](cg),
        'res': lambda bm, bp, ch, cg: 40
    }, {
        # if BMI = healthy and blood pressure = LOW and cholesterol = LOW
        'rule': lambda bm, bp, ch, cg: min(bmi['healthy'](bm), blp['low'](bp), cho['low'](ch)),
        'res': lambda bm, bp, ch, cg: 10
    }
]


def centre_of_area(bm, bp, ch, cg):
    products = 0
    weights = 0

    for rule in rules:
        weight = rule['rule'](bm, bp, ch, cg)
        product = weight * rule['res'](bm, bp, ch, cg)
        products += product
        weights += weight

    if weights != 0:
        return (products / weights)
    else:
        return 0


bm = int(sys.argv[1])
bp = int(sys.argv[2])
ch = int(sys.argv[3])
cg = int(sys.argv[4])

print('€', round(centre_of_area(bm, bp, ch, cg), 2))
