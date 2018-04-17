import random

word_dict = [
    "元芳-展昭",
    "福尔摩斯-工藤新一",
    "镜子-玻璃",
    "葡萄-提子",
    "天天向上-非诚勿扰",
    "纸巾-手帕",
    "作家-编剧",
    "小沈阳-宋小宝",
    "辣椒-芥末",
    "近视眼镜-隐形眼镜",
    "蜘蛛侠-蝙蝠侠",
    "包青天-狄仁杰",
    "铁观音-碧螺春",
    "油条-麻花",
    "干洗机-甩干机",
    "首尔-东京",
    "若曦-晴川",
    "端午节-中秋节",
    "江南style-最炫民族风",
    "刘诗诗-刘亦菲",
    "海豚-海狮",
    "节节高升-票房大卖",
    "梦境-幻想",
    "自行车-电动车",
    "大白兔-金丝猴",
    "反弹琵琶-乱弹棉花",
    "叉烧包-灌汤包",
    "成吉思汗-努尔哈赤",
    "图书馆-图书店",
    "董永-许仙",
    "果粒橙-鲜橙多",
    "烤肉-涮肉",
    "洗发露-护发素",
    "屌丝-宅男",
    "张韶涵-王心凌",
    "口香糖-木糖醇",
    "饺子-包子",
    "孟非-乐嘉",
    "沐浴露-沐浴盐",
    "流星花园-花样男子",
    "作文-论文",
    "榨菜丝-萝卜头",
    "谢娜-李湘",
    "气泡-水泡",
    "牛奶-豆浆",
    "盒饭-外卖",
    "泡泡糖-棒棒糖",
    "高跟鞋-增高鞋",
    "红烧牛肉面-香辣牛肉面",
    "语无伦次-词不达意",
    "蜘蛛侠-蜘蛛精",
    "玫瑰-月季",
    "麻婆豆腐-皮蛋豆腐",
    "何炅-维嘉",
    "状元-冠军",
    "勇往直前-全力以赴",
    "吉他-琵琶",
    "酸菜鱼-水煮鱼",
    "丑小鸭-灰姑娘",
    "淘宝-京东",
    "裸婚-闪婚",
    "鱼香肉丝-四喜丸子",
    "散热器-电风扇",
    "香港-台湾",
    "洗衣粉-皂角粉",
    "同学-同桌",
    "摩托车-电动车",
    "麦克风-扩音器",
    "水盆-水桶",
    "新年-跨年",
    "土豆粉-酸辣粉",
    "白菜-生菜",
    "胖子-肥肉",
    "蝴蝶-蜜蜂",
    "小品-话剧",
    "穿衣-试衣",
    "杭州-苏州",
    "反射-折射",
    "保安-保镖",
    "小矮人-葫芦娃",
    "剩女-御姐",
    "甄子丹-李连杰",
    "那英-韩红",
    "童话-神话",
    "鼠目寸光-井底之蛙",
    "面包-蛋糕",
    "热的快-热水器",
    "男朋友-前男友",
    "结婚-订婚",
    "手机-座机",
    "神雕侠侣-天龙八部",
    "婚纱-喜服",
    "降龙十八掌-九阴白骨爪",
    "唇膏-口红",
    "郭德纲-周立波",
    "贵妃醉酒-黛玉葬花",
    "夏家三千金-爱情睡醒了",
    "情人节-光棍节",
    "奖牌-金牌",
    "孟飞-乐嘉",
    "富二代-高富帅",
    "麻雀-乌鸦",
    "枕头-抱枕",
    "甄嬛传-红楼梦",
    "魔术师-魔法师",
    "梁山伯与祝英台-罗密欧与朱丽叶",
    "点烟器-打火机",
    "牛肉干-猪肉脯",
    "欲求不满-饥渴难耐",
    "欲火焚身-寂寞难耐",
    "玉米-小米",
    "小笼包-灌汤包",
    "谢娜张杰-邓超孙俪",
    "生活费-零花钱",
    "金庸-古龙",
    "橙子-橘子",
    "壁纸-贴画",
    "眉毛-胡须",
    "薰衣草-满天星",
    "赵敏-黄蓉",
    "公交-地铁",
    "十面埋伏-四面楚歌",
    "老佛爷-老天爷",
    "鸭舌帽-遮阳帽",
    "班主任-辅导员",
    "伐木工-木匠工",
    "双胞胎-龙凤胎",
    "老朋友-老男孩",
    "过山车-碰碰车",
    "警察-捕快",
    "汉堡包-肉夹馍",
    "王菲-那英",
    "推销-销售",
    "臭豆腐-粑粑",
    "买一送一-再来一瓶",
    "土豆-番茄"
]


class Player:
    def __init__(self, user, word, uc):
        self.user = user
        self.word = word
        self.uc = uc
        self.count = 0
        self.out = False


class Game:
    def __init__(self, players, win):
        self.name = "谁是卧底"
        self.players = []
        self.win = win
        word = random.choice(word_dict).split("-")
        rand = random.randint(0,1)
        if rand == 0:
            self.normal = word[0]
            self.undercover = word[1]
        else:
            self.normal = word[1]
            self.undercover = word[0]
        uc = random.randint(0, len(players) - 1)
        for i in range(len(players)):
            if i == uc:
                self.players.append(Player(players[i], self.undercover, True))
            else:
                self.players.append(Player(players[i], self.normal, False))

    def check(self):
        count = 0
        for i in self.players:
            if not i.out:
                count += 1
        return count <= self.win
