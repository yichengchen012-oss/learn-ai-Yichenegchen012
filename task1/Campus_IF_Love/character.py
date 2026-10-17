import text


class Character:
    def __init__(self, name, role, affinity=0):
        self.name = name
        self.role = role
        self.affinity = affinity
        self.dialogues = 0

    def talk(self):
        if self.dialogues >= len(text.DIALOGUES[self.name]):
            print(f"{self.name} 暂时没有更多的话要说了。")
            return
        
        print(f"你正在和{self.name}对话...")
        now_dialogues = text.DIALOGUES[self.name][self.dialogues]
        print(now_dialogues["text"])
        print(f"A:{now_dialogues["optionA"]}")
        print(f"B:{now_dialogues["optionB"]}")
        choice = input("请选择对话选项（A/B）：")
        if choice.upper() == "A":
            print(f"你选择了选项A：{now_dialogues["optionA"]}")
            self.change_affinity(5)
        elif choice.upper() == "B":
            print(f"你选择了选项B：{now_dialogues["optionB"]}")
            self.change_affinity(-5)
        else:
            print("无效输入，请重新选择。")
            return self.talk()
        self.dialogues += 1

        # TODO: 补充具体对话，对话内容可以从剧本里面截取 根据主人公的不同，使用不同的对话（你也可以根据好感度的不同/对话次数的不同 改变对话和选项）

    def give_gift(self):
        print(f"你想送给 {self.name} 什么礼物？")
        print(f"可选礼物：{list(text.GIFT_EFFECTS.keys())}")
        gift = input("请输入礼物名称：")
        if gift in text.GIFT_EFFECTS:
            print(f"你送给 {self.name} 一份 {gift}。")
            value = text.GIFT_EFFECTS[gift].get(self.name, text.GIFT_EFFECTS[gift].get("default"))
            self.change_affinity(value)
        else:
            print(f"{gift} 不是有效的礼物,请重新选择。")
            return self.give_gift()
        
        # TODO: 完成礼物好感度逻辑（送出不同礼物加不同的好感度） 并调用change_affinity（）函数 传入此次好感度变化的数值value

    def change_affinity(self, value:int):
        self.affinity += value
        print(f"{self.name} 的好感度变化 {value} -> 当前好感度：{self.affinity}")

    def check_ending(self):
        if self.affinity >= 100:
            print(f"恭喜！你和 {self.name} 的故事进入了结局线！")
            print(text.ENDINGS[self.name])
            return True
        return False
