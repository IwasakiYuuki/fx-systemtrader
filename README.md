# FXシステムトレード用リポジトリ
## 概要
機械学習基盤を用いて継続的にデータを収集・蓄積し定期的なモデルの学習・評価を行うことで，（ほぼ）全自動でFXのシステムトレードを行える基盤．

## ディレクトリ構造
```
.
├── README.md
├── argo_workflows      # Argo Workflowの各ワークフローなど
├── cloud_functions     # Cloud Functionsのソースコード
├── environments/(dev)  # Terraformのメインのコード
├── modules             # Terraformのモジュール
├── gke                 # GKEの初期設定（MLFlow・Argoサーバなど）
├── fst                 # fstディレクトリは以前使っていたが，今は特に使用していない
└── cloudbuild.yaml     # Cloud Buildの設定ファイル
```

## 現時点で実装した機能
- Cloud BuildとTerraformを使ってGitOps（というのかな？）
- FX（OANDA API）のデータを継続的に取得
- 取得したデータをBigQueryに蓄積
- GKEへのMLFlow・Argoサーバのデプロイ（機械学習用基盤）
- Argo Workflowの公式チュートリアル，Iris分類サンプル
- Workload IdentityによるGKEサービスアカウントからの権限付与

## TODO
- TwitterAPIからデータを取得するジョブを作成
- 取得したデータをBigQueryに蓄積する（差分更新）ジョブの作成
- データのクレンジング（クリーニング？）
  - 画像やURL付きのツイートを除く
  - 極端に短い・長い文字数のツイートを除く
  - などなど・・・
