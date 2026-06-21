from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)


class Post(models.Model):
    title=models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Knowledge(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE,related_name='knowledges')
    tags=models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    knowledge=models.ForeignKey(Knowledge, on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.text[:20]


class Like(models.Model):
    """
    「いいね」1件を表すモデル
    「どの投稿」に「どのユーザー」が押したか、を1行として記録する

    いいねの合計数は、この行を数えれば出せる(post.likes.count)
    """

    #どの投稿へのいいねか
    #related_name='likes' にしておくと、投稿側から post.likes で逆引きできる
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE, related_name='likes')

    #誰が押したか
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #いつ押したか(自動で今の時刻が入る)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #unique_together:この2つの組み合わせはDBの中で1組だけ、というルール
        #同じユーザーが同じ投稿に2回いいねできないように、ここで止めておく
        unique_together = ('knowledge', 'user')

    def __str__(self):
        #管理画面で「誰が→どの投稿に」を見やすくするための表示
        return f'{self.user.username} → {self.knowledge.title}'
    

