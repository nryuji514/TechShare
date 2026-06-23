# TechShare ER図（シンプル版・発表用）

データベースが情報をどう管理しているかを **ひと目で** 伝えるための、要点だけに絞ったER図です。
（「いいね」「タグ」は省略し、中心となる4つのテーブルだけを載せています）

---

## 全体のER図

```mermaid
---
config:
  layout: elk
  theme: base
  themeVariables:
    fontFamily: "Segoe UI, Meiryo, sans-serif"
    fontSize: "18px"
    lineColor: "#7a7a7a"
---
erDiagram
    ユーザー ||--o| プロフィール : "1対1（プロフィールを持つ）"
    ユーザー ||--o{ 記事         : "1対多（記事を書く）"
    ユーザー ||--o{ コメント     : "1対多（コメントする）"
    記事     ||--o{ コメント     : "1対多（コメントが付く）"

    ユーザー {
        int id PK "ユーザーID"
        string username UK "ユーザー名"
        string password "パスワード（暗号化）"
    }

    プロフィール {
        int id PK "プロフィールID"
        int user_id FK "どのユーザーのものか"
        string display_name "表示名"
        text bio "自己紹介"
        image avatar "プロフィール画像"
    }

    記事 {
        int id PK "記事ID"
        string title "タイトル"
        text content "本文"
        image image "添付画像"
        int author_id FK "書いた人（ユーザー）"
        datetime created_at "作成日時"
    }

    コメント {
        int id PK "コメントID"
        int knowledge_id FK "どの記事へのコメントか"
        int user_id FK "コメントした人"
        text text "コメント本文"
        datetime created_at "作成日時"
    }

    style ユーザー fill:#CFE2FF,stroke:#084298,color:#084298
    style プロフィール fill:#CFE2FF,stroke:#084298,color:#084298
    style 記事 fill:#D1E7DD,stroke:#0F5132,color:#0F5132
    style コメント fill:#F8D7DA,stroke:#842029,color:#842029
```

> **色の意味**：🟦 ユーザー系（ユーザー／プロフィール）・🟩 コンテンツ系（記事）・🟥 反応系（コメント）

---

## つながりの一覧

| つながり | 種類 | ひとことで言うと |
|----------|------|------------------|
| ユーザー ― プロフィール | 1対1 | 1人に1つの自己紹介 |
| ユーザー ― 記事 | 1対多 | 1人がたくさん投稿 |
| ユーザー ― コメント | 1対多 | 1人がたくさんコメント |
| 記事 ― コメント | 1対多 | 1記事にたくさんコメント |

---

## 記号の読み方（かんたん）

- **PK**＝主キー。その行を見分ける番号（だいたい `id`）。
- **FK**＝外部キー。別テーブルの行を指す番号。これでテーブル同士がつながる。
- **UK**＝一意キー。同じ値が2つ存在できない列。
- 線の **枝分かれしている側が「たくさん」**。
