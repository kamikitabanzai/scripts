# markdownテキストからwordドキュメントの作成について

## 前置き

### 制限事項
- 表のセルは結合出来ない  
(それが出来るmarkdown_php_extra というのもあるようですが、それでも横(行)の結合は出来ても縦(列)の結合は出来ません)
- ネストされた箇条書きは使わない  
(wordにした時のインデントをコントロールできない)

### 使いどころ
- 表や図が主体の成果物には向かない  
表はパイプで繋ぐだけですが、セルの結合が出来ない点は痛いです。
横(行)の結合は拡張機能で出来るものもあるみたいですが、縦は対応していません。
また図のサイズ調整がwordよりもしずらいため、図が多い場合も向かないかもしれません。

- 単純な表しか使わず、図も少ない成果物を作る際に向いている  
例えばCUIで進める構築手順書や、操作手順書などは大分効率的に進められると思います。

- ドラフト版の作成に適している  
最後まで markdown で管理したいところですが、
pandoc には制限が多いため細かいフォーマットの修正が出来ません。
図の位置やサイズ、ネストされた箇条書きにしたい場合など、
最後は word 側で修正する方が効率的(pythonでやるのに比べて)だと
感じました。
その代わり最初のドラフト版を作る際に使うのは効率的だと思います。

### 使っている技術
- markdown
- pandoc
- python(pyton-docx)
- gitlab

## 準備
### pandoc のインストール
- 以下ページの"Download the latest installer for Windowns(64-bit)"より
https://pandoc.org/installing.html

- インストール後、PATHを通してください。
https://qiita.com/shuhey/items/7ee0d25f14a997c9e285

### python-docx インストール
- pyhton 3ダウンロード  
インストール中にPATHも通せます。  
ref)  
https://www.python.org/downloads/


### python-docx インストール

clear-internetやVPN外から実施してください  
(社内ネットワークから実施する場合はプロキシを通す必要あり）

	python -m pip install --upgrade pip
	python -m pip install --upgrade python-docx
	python -m pip install --upgrade chardet


ref)  
https://python-docx.readthedocs.io/en/latest/user/install.html

### markdown editor のインストール

**必ずリアルタイムプレビュー機能のある markdown editor を使ってください**

markdown 書式のシンタックスエラーの修正に時間を取られては元も子もありません。word 化してからチェックだとめちゃくちゃ時間を取られます。  
それでは word のフォーマット修正が markdown のシンタックスエラーの修正に置き換わるだけです。  
使わなければ段落分けや改行のコントロールだけでもかなり苦労してしまいます。

いろいろ試しましたが、完璧なEditorはありません。
強いて言うならVisual Studio Code かBoostnoteか2択だと思います。

- Boostnote  
    - リアルタイムプレビューでmarkdown のテンプレートで凡例として使っている3つの書式、コードブロック、引用  、定義リストをサポート  
    - 画像のパスが変換されて出力される。
    - 画像のパスを直接記述出来ない
    - 画像のキャプションが表示されない
    - 拡張機能に乏しい
    - リアルタイムプレビューの表示位置が勝手にずれるのが、凄くストレス
- Visual Studio Code
    - リアルタイムプレビューで定義リストをサポートしていない
    - 画像のパスが変換されて表示されない
    - 画像のパスを直接記述出来る
    - 画像のキャプションが表示されない
    - いろいろ拡張機能がある(markdown書式のチェック機能など)

Visual Studio Code で設計理由の凡例として使う、定義リストの書式が使えない(Atom,Typoraも同様)点を致命的と感じましたが、他によいEditorがないのでしぶしぶ使っています。

#### appendix. Visual Studio Code のインストール手順
1. install  
https://code.visualstudio.com/download#

2. 日本語化  
https://qiita.com/nanamesincos/items/5c48ff88a4eeef0a8631

3. files.autoGuessEncoding の設定  
https://qiita.com/github129/items/edf1a2c0472fbe293f9c

4. リアルタイムプレビュー機能を使用  
http://sig9.hatenablog.com/entry/2017/03/14/120000



## markdown のフォーマットや関連ファイルのダウンロード

以下URLからダウンロードし、展開してください。

http://mm1v/nobutaka.taniuchi/edion-oci/-/archive/master/edion-oci-master.zip?path=template

19-11-30_Word_template.md

:   markdownのテンプレート。  
    これを編集してドキュメントを作成してください。


pydoc.py  

:    pandoc で指定できないWordのフォーマットの指定を行います。


current-directory\pandoc

:   refrence_pn.doc 配置ディレクトリ  
    Wordのフォーマットはこのディレクトリのreference_pn.docで指定しています。見出しのスタイルなどの修正が必要なときはこれを編集します。

current-directory\img

:   イメージファイル格納用ディレクトリ  
    ドキュメントに必要なイメージをここに配置します。
