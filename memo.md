장고 외래키 매핑은 다음과 같이 매핑할 수 있다.
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    
class Blog ( models.Model):
    admin = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_title = models.ForeignKey(Post, on_delete=models.CASCADE)
```
spring 처럼 cascade도 설정할 수 있고, 아이디값도 자동으로 생성해준다

## 관계
다른 ORM처럼 장고도 엔티티 간의 관계를 맺을 수 있다. 다대다, 다대일, 일대일 관계 모두 지원한다. 

```python
from django.db import models

class Manufacturer(models.Model):
    # ...
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # ...
```
자동차와 제조사간의 일대다 관계를 위와 같이 매핑할 수 있다. 

다대다 관계는 아래와 같이 선언할 수 있다. 
```python
from django.db import models

class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
```
토핑, 피자 어느쪽에나 관계 없이 다대다 관계를 명시할 수 있고, 다대다 관계 필드 명을 복수형으로 쓰는것이 권장된다. 다음과 같은 예시는 다대다 관계에서 중간테이블을 두는 예시이다.
```python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```
보면 `members = model.ManyToManyField(Person, through = 'Membership')` 이라는 코드가 있는데, 무슨 의미냐면 멤버십이 그룹과 person에 중간 테이블 역할을 한다는 것이다. 멤버십 테이블 안에는 조인한 날짜, 초대 이유등 여러가지 부가 정보를 넣을 수 있다. 

디비 연관관계 세팅도 알아보았으니, 디비 구조를 결정하고, 서비스 코드를 작성해 나가보자