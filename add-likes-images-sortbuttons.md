# チュートリアル：マイページのいいね数表示／画像投稿／並び替えボタンのデザイン統一

このチュートリアルでは、TechShare に次の3つの機能を追加する手順を説明します。

1. マイページ（`mypage.html`）の自分の投稿に、いいね数を表示する
2. 投稿（`Knowledge`）に画像を添付できるようにする
3. 記事一覧の「新着順」「いいね数順」ボタンを、サイトの他のボタン（ヘッダーのナビゲーションやいいねボタン）と同じデザインに揃える

それぞれ独立した機能なので、好きな順番で進めてOKです。コードは現在のリポジトリの状態（`knowledge/models.py` / `views.py` / `forms.py` / 各テンプレート・CSS）を前提にしています。

---

## 機能1：マイページの投稿に「いいね数」を表示する

### 現状
記事一覧（`knowledge_list.html`）と詳細ページ（`knowledge_detail.html`）はいいね数を表示していますが、マイページ（`mypage.html`）の投稿カードにはいいね数が出ていません。`Like` モデルは `Knowledge` に対して `related_name='likes'` を持っているので、`post.likes.count` で件数が取れます。

### Step 1: views.py の `mypage` でいいね数を集計する

1件ずつ `post.likes.count()` をテンプレートで呼ぶと投稿数だけクエリが飛んでしまうので、一覧ページと同じように `annotate(Count('likes'))` でまとめて集計します。

```python
# knowledge/views.py

# ファイル先頭で既に import 済み: from django.db.models import Count

@login_required
def mypage(request):
    Profile.objects.get_or_create(user=request.user)
    posts = Knowledge.objects.filter(author=request.user).order_by('-created_at')
    # 各投稿のいいね数を集計（knowledge_list と同じやり方）
    posts = posts.annotate(like_count=Count('likes'))
    return render(request, 'mypage.html', {'posts': posts})
```

### Step 2: mypage.html にいいね数を表示する

`post-meta` の中（日付の隣あたり）に追記します。

```html
<!-- knowledge/templates/mypage.html -->
<div class="post-meta">
    <span class="post-date">
        {{ post.created_at|date:"Y/m/d H:i" }}
    </span>

    <span class="post-likes">❤️ {{ post.like_count }}</span>

    <span class="post-tags">
        {% for tag in post.tags.all %}
            <span class="tag">#{{ tag.name }}</span>
        {% endfor %}
    </span>
</div>
```

### Step 3: mypage.css にスタイルを追加する

```css
/* knowledge/static/knowledge/css/mypage.css の末尾などに追加 */

.post-likes {
    margin-left: 10px;
    color: #e0527a;
    font-weight: bold;
    font-size: 13px;
}
```

これで `post.likes.count` ではなく `post.like_count`（annotateされた値）を表示するので、N+1クエリにならずに済みます。

---

## 機能2：投稿に画像を添付できるようにする

### 現状
`Profile.avatar` は `ImageField` で実装済み（Pillow も venv にインストール済み: `pillow-10.4.0`）。同じ仕組みを `Knowledge` モデルにも追加します。

### Step 0: requirements.txt に Pillow を明記する

`Profile.avatar` のために実際には既に動いていますが、`requirements.txt` には載っていません。今後 `pip install -r requirements.txt` で環境を作る人が `ImageField` を使えるように、明記しておきます。

```text
# requirements.txt
Django==4.2.30
pymysql==1.1.2
python-dotenv==1.0.1
Pillow==10.4.0
```

### Step 1: models.py に image フィールドを追加する

```python
# knowledge/models.py
class Knowledge(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='knowledge_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledges')
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
```

`blank=True, null=True` にして、画像なしでも投稿できるようにしています（必須にすると既存の投稿が壊れます）。

### Step 2: マイグレーションを作成・適用する

```bash
python manage.py makemigrations knowledge
python manage.py migrate
```

`knowledge/migrations/000X_knowledge_image.py` のようなファイルが自動生成されます。

### Step 3: forms.py の KnowledgeForm に image を追加する

```python
# knowledge/forms.py
class KnowledgeForm(forms.ModelForm):
    class Meta:
        model = Knowledge
        fields = ['title', 'content', 'image']
```

### Step 4: views.py で request.FILES を渡す

画像アップロードを伴うフォームは `request.FILES` も渡さないと保存されません。`knowledge_create` と `knowledge_edit` の両方を直します。

```python
# knowledge/views.py
@login_required
def knowledge_create(request):
    if request.method == 'POST':
        form = KnowledgeForm(request.POST, request.FILES)  # ← request.FILES を追加
        ...

@login_required
def knowledge_edit(request, pk):
    post = get_object_or_404(Knowledge, pk=pk, author=request.user)

    if request.method == 'POST':
        form = KnowledgeForm(request.POST, request.FILES, instance=post)  # ← request.FILES を追加
        ...
```

### Step 5: knowledge_form.html に enctype を追加する

ファイルを送るフォームには `enctype="multipart/form-data"` が必須です（`avatar_upload` のフォームも同様の指定をしています）。

```html
<!-- knowledge/templates/knowledge_form.html -->
<form method="post" action="" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    ...
</form>
```

`{{ form.as_p }}` が image フィールドのファイル選択UIも自動で出してくれるので、テンプレート側はこれだけで大丈夫です。

### Step 6: 詳細ページに画像を表示する

```html
<!-- knowledge/templates/knowledge_detail.html -->
<!-- 「内容：」の段落の下あたりに追加 -->
{% if post.image %}
    <img src="{{ post.image.url }}" class="post-image" alt="{{ post.title }}">
{% endif %}
```

```css
/* knowledge/static/knowledge/css/detail.css に追加 */
.post-image {
    max-width: 100%;
    border-radius: 12px;
    margin: 16px 0;
}
```

### Step 7: 一覧ページにサムネイルを表示する（任意）

```html
<!-- knowledge/templates/knowledge_list.html -->
<!-- card-author の下、card-excerpt の上あたりに追加 -->
{% if post.image %}
    <img src="{{ post.image.url }}" class="card-image" alt="{{ post.title }}">
{% endif %}
```

```css
/* knowledge/static/knowledge/css/list.css に追加 */
.card-image {
    width: 100%;
    max-height: 220px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 12px;
}
```

開発環境では `config/urls.py` に既に `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` が `DEBUG=True` 時に設定済みなので、追加の設定なしで `/media/knowledge_images/...` が表示できます。

---

## 機能3：並び替えボタンをサイトのデザインに統一する

### 現状
`knowledge_list.html` の「新着順」「いいね数順」は `<a>` タグの素のリンクに、インラインスタイルと `activate` という未使用クラス（CSSにルールが無いので何も効いていない）が付いているだけで、見た目がサイトの他のボタン（ヘッダーの `nav-link` や記事カードの `like-btn`）と合っていません。

### Step 1: knowledge_list.html のマークアップを直す

クラス名をヘッダーの選択状態と同じ命名（`active`）に揃え、インラインスタイルをCSSクラスに置き換えます。

```html
<!-- knowledge/templates/knowledge_list.html -->
<div class="sort-links">
    並び替え：
    <a href="?q={{ search_keyword }}&sort=new"
       class="sort-btn {% if sort == 'new' %}active{% endif %}">新着順</a>
    <a href="?q={{ search_keyword }}&sort=likes"
       class="sort-btn {% if sort == 'likes' %}active{% endif %}">いいね数順</a>
</div>
```

(`activate` → `active` への変更点に注意。ヘッダーの `.nav-link.active` と命名を揃えています。)

### Step 2: list.css にボタンのスタイルを追加する

サイト全体で使われている「枠線つきの丸ピル型ボタン、選択中は青背景」というパターン（`nav-link.active` や `like-btn`）に合わせます。

```css
/* knowledge/static/knowledge/css/list.css に追加 */

.sort-links {
    margin-top: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #777;
}

.sort-btn {
    color: #444;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 999px;
    border: 1px solid #e0e0e0;
    background: #fff;
    transition: 0.2s;
}

.sort-btn:hover {
    background: #e8f1ff;
    color: #2563eb;
    border-color: #c7dcff;
}

.sort-btn.active {
    background: #2563eb;
    color: #fff;
    border-color: #2563eb;
}
```

これでヘッダーの選択中タブ（青背景）や、いいねボタンのピル型と同じ視覚言語になります。

---

## 動作確認チェックリスト

- [ ] `python manage.py makemigrations` → `migrate` を実行してエラーが出ない
- [ ] マイページで自分の投稿カードに `❤️ 数字` が表示される
- [ ] 新規投稿フォームから画像を選んで投稿し、詳細ページ・一覧ページに画像が表示される
- [ ] 画像なしで投稿してもエラーにならない（`blank=True, null=True` の確認）
- [ ] 記事一覧の「新着順」「いいね数順」が、ヘッダーのタブと同じ見た目のボタンになり、選択中のものだけ青くなる
- [ ] 並び替えを切り替えても検索キーワード（`q`）が保持される

## まとめ

- いいね数表示は `annotate(Count('likes'))` をビューに足すだけで、テンプレートは1行追加するだけでした。
- 画像投稿は「モデルに `ImageField` を足す → マイグレーション → フォームに `fields` 追加 → ビューで `request.FILES` を渡す → テンプレートに `enctype` を追加」という、`Profile.avatar` と同じ5点セットがポイントです。
- ボタンのデザイン統一は、機能追加ではなくCSSクラスの命名をサイト内の既存パターン（`.nav-link.active` や `.like-btn`）に合わせるだけで解決します。
