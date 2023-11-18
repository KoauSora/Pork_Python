from AI_Part.douzero.env.game import GameEnv, RealCard2EnvCard
from AI_Part.douzero.evaluation.deep_agent import DeepAgent
import threading

AllEnvCard = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7,
              8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12,
              12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 17, 17, 17, 17, 20, 30]


class AI_part:
    """
    调用顺序，按顺序来
    """

    def __init__(self):
        # 线程阻塞函数
        self.ready = threading.Event()

        # 回合数
        self.order = 0
        # 一些手牌内容
        self.ai_players = [0, 0]
        self.env = None
        self.play_order = None
        self.card_play_data_list = None
        # 位置
        self.user_position_code = None
        self.user_position = None
        #
        self.three_landlord_cards_env = None
        self.three_landlord_cards_real = None
        self.other_hand_cards = None
        self.other_played_cards_env = None
        self.other_played_cards_real = None
        self.user_hand_cards_env = None
        self.user_hand_cards_real = None

        # 玩家
        self.LPlayer = None
        self.Player = None
        self.RPlayer = None

        # 输出内容
        self.cards_out = ""
        self.win_rate = ""
        self.Players = [self.RPlayer, self.Player, self.LPlayer]

        # 模型路径
        self.model_path = {
            'landlord': "C:\\Users\\lenovo\\Desktop\\Pork_Python\\AI_Part\\douzero\\baselines\\landlord.ckpt",
            'landlord_up': "C:\\Users\\lenovo\\Desktop\\Pork_Python\\AI_Part\\douzero\\baselines\\landlord_up.ckpt",
            'landlord_down': "C:\\Users\\lenovo\\Desktop\\Pork_Python\\AI_Part\\douzero\\baselines\\landlord_down.ckpt"
        }

    def init_cards(self, user_hand_card_in, user_position_in, three_landlord_cards_real):
        """
        :param user_position_in: 'landlord_up', 'landlord', 'landlord_down'
        :param three_landlord_cards_real: 同下
        :param user_hand_card_in: example :假设有 2 个 2 ，两个A ，三个 3 ，则输入[22AA333]
        :return:
        """
        # 玩家手牌
        self.user_hand_cards_real = user_hand_card_in
        self.user_hand_cards_env = [RealCard2EnvCard[c] for c in list(self.user_hand_cards_real)]
        # 其他玩家出牌
        self.other_played_cards_real = ""
        self.other_played_cards_env = []
        # 其他玩家手牌（整副牌减去玩家手牌，后续再减掉历史出牌）
        self.other_hand_cards = []
        # 三张底牌
        self.three_landlord_cards_real = three_landlord_cards_real
        self.three_landlord_cards_env = [RealCard2EnvCard[c] for c in list(self.three_landlord_cards_real)]
        # 玩家角色代码：0-地主上家, 1-地主, 2-地主下家
        self.user_position = user_position_in
        if self.user_position == "landlord":
            self.user_position_code = 1
        elif self.user_position == "landlord_up":
            self.user_position_code = 0
        elif self.user_position == "landlord_down":
            self.user_position_code = 2
        # self.user_position_code = [0, 1, 2][self.user_position]
        # 开局时三个玩家的手牌
        self.card_play_data_list = {}
        # 出牌顺序：0-玩家出牌, 1-玩家下家出牌, 2-玩家上家出牌
        # self.play_order = 0

        for i in set(AllEnvCard):
            self.other_hand_cards.extend([i] * (AllEnvCard.count(i) - self.user_hand_cards_env.count(i)))
        self.card_play_data_list.update({
            'three_landlord_cards': self.three_landlord_cards_env,
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 0) % 3]:
                self.user_hand_cards_env,
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 1) % 3]:
                self.other_hand_cards[0:17] if (self.user_position_code + 1) % 3 != 1 else self.other_hand_cards[17:],
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 2) % 3]:
                self.other_hand_cards[0:17] if (self.user_position_code + 1) % 3 == 1 else self.other_hand_cards[17:]
        })

    def init_players(self):
        self.ai_players[0] = self.user_position
        self.ai_players[1] = DeepAgent(self.user_position, self.model_path[self.user_position])

    def init_Env(self):
        self.env = GameEnv(self.ai_players)
        self.env.card_play_init(self.card_play_data_list)

    def update_player_order(self, player_order_in):
        """

        :param player_order_in: 出牌顺序：0-玩家先出牌, 1-玩家下家先出牌, 2-玩家上家先出牌
        :return:
        """
        self.play_order = player_order_in

    def start_predict(self, down_in, up_in):
        """
        :param down_in: 下家牌
        :param up_in: 上家牌
        :return: None
        """

        if self.play_order == 0:
            if self.order == 0:

                action_message = self.env.step(self.user_position)

                self.cards_out = action_message["action"] if action_message["action"] else "不出"
                self.win_rate = action_message["win_rate"]

                self.order += 1
                # self.ready.set()  # 要改
            elif self.order != 0:

                self.other_played_cards_real = down_in
                self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
                self.env.step(self.user_position, self.other_played_cards_env)

                self.other_played_cards_real = up_in
                self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
                self.env.step(self.user_position, self.other_played_cards_env)

                action_message = self.env.step(self.user_position)

                self.cards_out = action_message["action"] if action_message["action"] else "不出"
                self.win_rate = action_message["win_rate"]

                self.order += 1
                # self.ready.set()
        elif self.play_order == 1:

            self.other_played_cards_real = down_in
            self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
            self.env.step(self.user_position, self.other_played_cards_env)

            self.other_played_cards_real = up_in
            self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
            self.env.step(self.user_position, self.other_played_cards_env)

            action_message = self.env.step(self.user_position)
            self.cards_out = action_message["action"] if action_message["action"] else "不出"
            self.win_rate = action_message["win_rate"]

            self.order += 1
            # self.ready.set()
        elif self.play_order == 2:
            if self.order != 0:

                self.other_played_cards_real = up_in
                self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
                self.env.step(self.user_position, self.other_played_cards_env)

                action_message = self.env.step(self.user_position)
                self.cards_out = action_message["action"] if action_message["action"] else "不出"
                self.win_rate = action_message["win_rate"]

                # self.ready.set()
                self.order += 1
            elif self.order != 0:

                self.other_played_cards_real = down_in
                self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
                self.env.step(self.user_position, self.other_played_cards_env)

                self.other_played_cards_real = up_in
                self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
                self.env.step(self.user_position, self.other_played_cards_env)

                action_message = self.env.step(self.user_position)
                self.cards_out = action_message["action"] if action_message["action"] else "不出"
                self.win_rate = action_message["win_rate"]

                # self.ready.set()
                self.order += 1

    def get_cards_out(self):
        return self.cards_out

    def get_win_rate(self):
        return self.win_rate
