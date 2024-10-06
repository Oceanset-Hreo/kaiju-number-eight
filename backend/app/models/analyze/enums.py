from enum import Enum


class EconomicCrops(Enum):
    WETLAND_RICE = "wetland rice"  # 水稻
    MAIZE = "maize"  # 玉米
    WHEAT = "wheat"  # 小麥
    SOYBEAN = "soybean"  # 大豆
    COTTON = "cotton"  # 棉花
    SUGARCANE = "sugarcane"  # 甘蔗
    SUGARBEET = "sugarbeet"  # 甜菜
    GROUNDNUT = "groundnut"  # 花生
    POTATO = "potato"  # 馬鈴薯
    BANANA = "banana"  # 香蕉
    COFFEE = "coffee"  # 咖啡
    TEA = "tea"  # 茶
    COCOA = "cocoa"  # 可可

    # TOBACCO = "tobacco"  # 煙草
    # RUBBER = "rubber"  # 橡膠
    # APPLE = "apple"  # 蘋果
    # OLIVES = "olives"  # 橄欖
    # TOMATOES = "tomatoes"  # 番茄
    # PEPPERS = "peppers"  # 辣椒
    # WINE_GRAPES = "wine grapes"  # 葡萄酒用葡萄
    # BARLEY = "barley"  # 大麥
    # OATS = "oats"  # 燕麥
    # SORGHUM = "sorghum"  # 高粱
    # MILLET = "millet"  # 小米
    # LAVENDER = "lavender"  # 薰衣草
    # FIGS = "figs"  # 無花果
    # ALMONDS = "almonds"  # 杏仁
    # WALNUTS = "walnuts"  # 核桃
    # PISTACHIOS = "pistachios"  # 開心果
    # HAZELNUTS = "hazelnuts"  # 榛子
    # CHESTNUTS = "chestnuts"  # 栗子
    # PECANS = "pecans"  # 山核桃
    # MACADAMIA = "macadamia"  # 夏威夷果
    # PINEAPPLE = "pineapple"  # 鳳梨
    # MANGO = "mango"  # 芒果
    # PAPAYA = "papaya"  # 木瓜
    # AVOCADO = "avocado"  # 酪梨
    # BERRIES = "berries"  # 莓果
    # CITRUS = "citrus"  # 柑橘
    # BANANA = "banana"  # 香蕉
    # PEAR = "pear"  # 梨
    # PEACH = "peach"  # 桃
    # PLUM = "plum"  # 李子
    # CHERRY = "cherry"  # 櫻桃


class AnalyzerTypes(Enum):
    AI = "AI"
    RULE_BASED = "RuleBased"
    STATISTICS = "Statistics"
