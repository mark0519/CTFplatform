# CTFplatform
 A simple CTF platform

## TodoList

- [ ] home
- [ ] about
- [ ] admin
- [ ] challenges
- [ ] login & register
- [ ] scoreboard
- [ ] teams
- [ ] users
- [ ] me

## 启动方式
```shell
set FLASK_APP=CTF
set FLASK_ENV=development
flask run
```

```shell
# 每台设备需要运行一次
flask shell
from CTF import db
db.drop_all()
```