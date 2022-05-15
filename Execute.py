from BasicDef import Write,Read,Indention
import re

StartLeft = 2#チェストの左から何行目からアイテムの配置を始めるか(0,1,2...)

BoardSizeH, BoardSizeV = 5, 5#コードネームの盤面のサイズ
ChestSizeH = 9#チェストの1行の大きさ
MCNameSpace = 'minecraft:'#マインクラフト名前空間(アイテムIDに付与する)
SrcHTML = Read('InputSource.txt')#ソースコードのテキストファイル読み込み
ItemListJP = Read('Resources/ItemListJP.txt')#日本語のアイテムリスト読み込み
ItemList = Read('Resources/ItemList.txt')#英語のアイテムリスト読み込み
CommandBase = Read('Resources/CommandBase.txt')#summonコマンドの読み込み
CommandNBT = Read('Resources/CommandNBT.txt')#Itemsのモジュール読み込み

#一つのボタンの前後の文字列
TagBefore, TagAfter = r'<main class="absolute z-50 pointer-events-none"', r'</div></section></div></div>'
#ボタン内の位置情報の前後の文字列
PosBefore, PosMiddle, PosAfter = r'style="left: ', r'px; top: ', r'px; width'
#ボタン内のラベル情報の前後の文字列
NameBefore, NameAfter = r'break-all; opacity: 1;">', r'</div></section></div></div>'
#正規表現の作成
ButtonCuttingWords, PosCuttingWords, NameCuttingWords = TagBefore + '.*?' + TagAfter, PosBefore + '.*?' + PosAfter, NameBefore + '.*?' + NameAfter
FormattedButtonList = []#ボタンの位置とラベルの整形済みのリスト

def FormatButtonData(SourceCode):#ソースコードから、ボタンの位置情報とラベルを抜き出して配列に収める
  ButtonRawList = re.findall(ButtonCuttingWords, SourceCode)#パターンに当てはまるものを全て抽出
  ButtonList = []#ボタンの位置情報とラベルを格納する配列
  for i in range(len(ButtonRawList)):
    Positions = str(re.search(PosCuttingWords,ButtonRawList[i]).group(0)).replace(PosBefore,'').replace(PosAfter,'').split(PosMiddle)
    Name = str(re.search(NameCuttingWords,ButtonRawList[i]).group(0)).replace(NameBefore,'').replace(NameAfter,'')
    FormattedOneButtonData = [Positions[0],Positions[1],Name]
    ButtonList.append(FormattedOneButtonData)
  return ButtonList

def SortFormattedList(List):#ボタンの位置情報ラベルの配列をソートし、位置情報の数値を消す
  SortedList = sorted(List, key=lambda x: (float(x[1]),float(x[0])))
  LabelList = [['' for i in range(BoardSizeH)] for j in range(BoardSizeV)]
  for i in range(BoardSizeH):
    for i2 in range(BoardSizeV):
      Index = i * BoardSizeH + i2
      LabelList[i][i2] = SortedList[Index][-1]
  return LabelList

def ConvertToItemID(List):#アイテムの日本語名の配列を与えたら、それをidの配列に変換する
  ItemListArray, ItemListJPArray = ItemList.split(Indention), ItemListJP.split(Indention)
  for i in range(BoardSizeH):
    for i2 in range(BoardSizeV):
      Label = List[i][i2]
      Index = ItemListJPArray.index(Label)
      List[i][i2] = MCNameSpace + ItemListArray[Index]
  return List

def NBTConverter(IDList):#アイテムのidの配列をNBTの列に変換して出力する
  LeftChestNBTs, RightChestNBTs = [], []
  for i in range(BoardSizeH):
    if 0 <= i and i <= 2:#左側のチェストデータを格納していく
      for i2 in range(BoardSizeV):
        ID, SlotNumber = IDList[i][i2], StartLeft + ChestSizeH * i + i2
        NBT = CommandNBT.replace('アイテムID',ID).replace('スロット番号',str(SlotNumber))
        LeftChestNBTs.append(NBT)
    else:
      for i2 in range(BoardSizeV):#右側のチェストデータを格納していく
        ID, SlotNumber = IDList[i][i2], StartLeft + ChestSizeH * (i - 3) + i2
        NBT = CommandNBT.replace('アイテムID',ID).replace('スロット番号',str(SlotNumber))
        RightChestNBTs.append(NBT)
  LeftItems, RightItems = ','.join(LeftChestNBTs), ','.join(RightChestNBTs)
  Command = CommandBase.replace('左側のチェストのアイテム',LeftItems).replace('右側のチェストのアイテム',RightItems)
  Write(Command,'Output.txt')

# 実行関数
def Execute():
  Write('','Output.txt')#出力ファイルの初期化
  FormattedButtonList = FormatButtonData(SrcHTML)
  FormattedButtonList = SortFormattedList(FormattedButtonList)
  FormattedButtonList = ConvertToItemID(FormattedButtonList)
  NBTConverter(FormattedButtonList)

Execute()