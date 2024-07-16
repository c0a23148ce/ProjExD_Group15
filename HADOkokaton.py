import math
import os
import random
import sys
import time
import pygame as pg


WIDTH = 1108  # ゲームウィンドウの幅
HEIGHT = 700  # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def check_bound_player1(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトがコート内orコート外を判定し，真理値タプルを返す関数
    引数：CharaのRect
    戻り値：横方向，縦方向のはみ出し判定結果（コート内：True／コート外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < WIDTH/2+2 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 124 or 680 < obj_rct.bottom:
        tate = False
    return yoko, tate


def check_bound_player2(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトがコート内orコート外を判定し，真理値タプルを返す関数
    引数：CharaのRect
    戻り値：横方向，縦方向のはみ出し判定結果（コート内：True／コート外：False）
    """
    yoko, tate = True, True
    if obj_rct.right > WIDTH/2+3 or 0 > obj_rct.left:
        yoko = False
    if obj_rct.top < 124 or 680 < obj_rct.bottom:
        tate = False
    return yoko, tate


class Chara_1(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    右側に描画されるキャラクター、青いこうかとん
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        画像Surfaceを生成する
        引数1 num：キャラクター画像ファイル名の番号
        引数2 xy：キャラクター画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 1.5)
        img = pg.transform.flip(img0, True, False)  # デフォルトのキャラクター

        self.imgs = {
            (+1, 0): img,  # 右
            (+1, -1): pg.transform.rotozoom(img, 45, 1.0),  # 右上
            (0, -1): pg.transform.rotozoom(img0, -90, 1.0),  # 上
            (-1, -1): pg.transform.rotozoom(img0, -45, 1.0),  # 左上
            (-1, 0): img0,  # 左
            (-1, +1): pg.transform.rotozoom(img0, 45, 1.0),  # 左下
            (0, +1): pg.transform.rotozoom(img0, 90, 1.0),  # 下
            (+1, +1): pg.transform.rotozoom(img, -45, 1.0),  # 右下
        }
        self.dire = (-1, 0)
        self.image = self.imgs[self.dire]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 8

    def change_img(self, num: int, screen: pg.Surface):
        """
        画像を切り替え，画面に転送する
        引数1 num：キャラクター画像ファイル名の番号
        引数2 screen：画面Surface
        """
        
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 1.5)
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてキャラクターを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rect.move_ip(self.speed*sum_mv[0], self.speed*sum_mv[1])
        if check_bound_player1(self.rect) != (True, True):
            self.rect.move_ip(-self.speed*sum_mv[0], -self.speed*sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        screen.blit(self.image, self.rect)


class Chara_2(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    左側に描画される、黄色のこうかとん
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_w: (0, -1),
        pg.K_s: (0, +1),
        pg.K_a: (-1, 0),
        pg.K_d: (+1, 0),
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        画像Surfaceを生成する
        引数1 num：キャラクター画像ファイル名の番号
        引数2 xy：キャラクター画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 1.5)
        img = pg.transform.flip(img0, True, False)  # デフォルトのキャラクター
        self.imgs = {
            (+1, 0): img,  # 右
            (+1, -1): pg.transform.rotozoom(img, 45, 1.0),  # 右上
            (0, -1): pg.transform.rotozoom(img, 90, 1.0),  # 上
            (-1, -1): pg.transform.rotozoom(img0, -45, 1.0),  # 左上
            (-1, 0): img0,  # 左
            (-1, +1): pg.transform.rotozoom(img0, 45, 1.0),  # 左下
            (0, +1): pg.transform.rotozoom(img, -90, 1.0),  # 下
            (+1, +1): pg.transform.rotozoom(img, -45, 1.0),  # 右下
        }
        self.dire = (+1, 0)
        self.image = self.imgs[self.dire]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 8

    def change_img(self, num: int, screen: pg.Surface):
        """
        画像を切り替え，画面に転送する
        引数1 num：キャラクター画像ファイル名の番号
        引数2 screen：画面Surface
        """
        
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 1.5)
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてキャラクターを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rect.move_ip(self.speed*sum_mv[0], self.speed*sum_mv[1])
        if check_bound_player2(self.rect) != (True, True):
            self.rect.move_ip(-self.speed*sum_mv[0], -self.speed*sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        screen.blit(self.image, self.rect)


class Beam_1(pg.sprite.Sprite):
    """
    キャラクター１のビームに関するクラス
    """
    def __init__(self, chara: Chara_1):
        """
        ビーム画像Surfaceを生成する
        引数 bird：ビームを放つキャラクター
        """
        super().__init__()
        self.vx, self.vy = chara.dire
        angle = math.degrees(math.atan2(-self.vy, self.vx))
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/beam.png"), angle, 1.5)
        self.vx = math.cos(math.radians(angle))
        self.vy = -math.sin(math.radians(angle))
        self.rect = self.image.get_rect()
        self.rect.centery = chara.rect.centery+chara.rect.height*self.vy
        self.rect.centerx = chara.rect.centerx+chara.rect.width*self.vx
        self.speed = 10

    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(self.speed*self.vx, self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()


class Beam_2(pg.sprite.Sprite):
    """
    キャラクター２のビームに関するクラス
    """
    def __init__(self, chara: Chara_2):
        """
        ビーム画像Surfaceを生成する
        引数 bird：ビームを放つキャラクター
        """
        super().__init__()
        self.vx, self.vy = chara.dire
        angle = math.degrees(math.atan2(-self.vy, self.vx))
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/beam2.png"), angle, 1.5)
        self.vx = math.cos(math.radians(angle))
        self.vy = -math.sin(math.radians(angle))
        self.rect = self.image.get_rect()
        self.rect.centery = chara.rect.centery+chara.rect.height*self.vy
        self.rect.centerx = chara.rect.centerx+chara.rect.width*self.vx
        self.speed = 10

    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(self.speed*self.vx, self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()


class Explosion(pg.sprite.Sprite):
    """
    爆発に関するクラス
    """
    def __init__(self, obj: Chara_1|Chara_2, life: int):
        
        # 爆弾が爆発するエフェクトを生成する
        # 引数1 obj：爆発するキャラクター
        # 引数2 life：爆発時間
        
        super().__init__()
        img = pg.image.load(f"fig/explosion.gif")
        self.imgs = [img, pg.transform.flip(img, 1, 1)]
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(center=obj.rect.center)
        self.life = life

    def update(self):
        
        # 爆発時間を1減算した爆発経過時間_lifeに応じて爆発画像を切り替えることで
        # 爆発エフェクトを表現する
        
        self.life -= 1
        self.image = self.imgs[self.life//10%2]
        if self.life < 0:
            self.kill()


class Hp_bar:
    """
    HPバーの表示に関するクラス
    """
    def __init__(self):
        """
        HPバー画像Surfaceを生成する
        """
        self.hp_rct = [WIDTH/2-525,25]
        self.hp_img = pg.image.load(f"fig/hp2.png") #hpバー
        self.hp_img = pg.transform.scale(self.hp_img, (1052, 100)) #hpバー画像のサイズ調整 
        self.time = 0
    
    def update(self, screen: pg.Surface):
        """
        経過時間表示
        引数 screen：画面Surface
        """
        self.black = pg.Surface((90, 27)) #hpバーの元画像も数字を消すためのsurfac
        screen.blit(self.hp_img, self.hp_rct) #hpバー表示
        pg.draw.rect(self.black,(0, 0, 0), (0, 0, WIDTH-599, 100)) #黒四角形を生成
        screen.blit(self.black, [WIDTH-599, 60]) #黒四角形表示
        fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        txt = fonto.render(str(self.time//50), True, (255, 0, 0))
        self.time += 1
        if self.time <= 500: #1桁の時
            screen.blit(txt, [WIDTH/2-5, 58])
        elif 500 < self.time <= 5000: #2桁の時
            screen.blit(txt, [WIDTH/2-12, 58])
        elif 5000 < self.time <= 49950: #3桁の時
            screen.blit(txt, [WIDTH/2-20, 58])
        else: #上記以外の時(999以上の時)
            max = fonto.render(str(999), True, (255, 0, 0)) #999で固定
            screen.blit(max, [WIDTH/2-20, 58])


class Player1_hp:
    """
    プレイヤー1のHPに関するクラス
    """
    def __init__(self):
        """
        残りHPを計数
        """
        self.hp_value = 464  #現在のhp
        self.hp_xy = [WIDTH-499, 65]

    def update(self, screen: pg.Surface):
        """
        横464縦16のHPバーSurfaceを生成する
        爆弾に当たった時にHPの四角形を更新
        引数 screen：画面Surface
        """
        self.hp = pg.Surface((464, 16)) #player1のHPバーSurfaceを生成
        pg.draw.rect(self.hp,(0, 255, 0), (0, 0, self.hp_value, 25)) #残りHPを更新
        screen.blit(self.hp, self.hp_xy) #残りHPを表示


class Player2_hp:
    """
    プレイヤー2のHPに関するクラス
    """
    def __init__(self):
        """
        被ダメージを計数
        """
        self.damage_value = 0  #被ダメージ
        self.hp_xy = [40, 65] 

    def update(self, screen: pg.Surface):
        """
        横461縦16のHPバーSurfaceを生成する
        爆弾に当たった時にHPの四角形を更新
        引数 screen：画面Surface
        """
        self.hp = pg.Surface((461, 16)) #player2のHPバーSurfaceを生成
        pg.draw.rect(self.hp,(0, 255, 0), (self.damage_value, 0, 461, 25)) #残りHPを更新
        screen.blit(self.hp, self.hp_xy) #残りHPを表示


def main():
    pg.display.set_caption("HADOU!!こうかとん!!")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"fig/background.jpg")

    charas1 = Chara_1(3, (WIDTH*3/4+20, HEIGHT/2+50))
    charas2 = Chara_2(32, (WIDTH/4-35, HEIGHT/2+45))
    beams1 = pg.sprite.Group()
    beams2 = pg.sprite.Group()
    exps = pg.sprite.Group()

    tmr = 0
    clock = pg.time.Clock()
    player1_hp = Player1_hp()
    player2_hp = Player2_hp()
    hp_bar = Hp_bar()
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_RSHIFT:
                beams1.add(Beam_1(charas1))# ビーム発射！
                
            if event.type == pg.KEYDOWN and event.key == pg.K_LSHIFT:
                beams2.add(Beam_2(charas2))# ビーム発射！
        screen.blit(bg_img, [0, 0])
        
        # chara1とビームの当たり判定
        if len(pg.sprite.spritecollide(charas1, beams2, True)) != 0:
            player1_hp.hp_value -= 50 #HPを50減らす
            exps.add(Explosion(charas1, 100))  # 爆発エフェクト
            if player1_hp.hp_value <= 0: #残りHPが0以下の時
                exps.add(Explosion(charas1, 100))  # 爆発エフェクト
                charas2.change_img(62, screen)  # こうかとん喜びエフェクト
                charas1.change_img(8, screen) # こうかとん悲しみエフェクト
                hp_bar.update(screen)
                player1_hp.update(screen)
                player2_hp.update(screen)
                pg.display.update()
                time.sleep(2)
                return
        
        # chara2とビームの当たり判定
        if len(pg.sprite.spritecollide(charas2, beams1, True)) != 0:
            player2_hp.damage_value += 50 #被ダメージを50増やす
            exps.add(Explosion(charas2, 100))  # 爆発エフェクト
            if player2_hp.damage_value >= 461: #被ダメージがHPを超えた時
                exps.add(Explosion(charas2, 100))  # 爆発エフェクト
                charas1.change_img(6, screen)  # こうかとん喜びエフェクト
                charas2.change_img(82, screen) # こうかとん悲しみエフェクト
                hp_bar.update(screen)
                player1_hp.update(screen)
                player2_hp.update(screen)
                pg.display.update()
                time.sleep(2)
                return

        # 座標確認用(座標を確認したいときに使ってね！)
        # line = pg.Surface((WIDTH, HEIGHT))
        # pg.draw.line(screen, (255, 0, 0), (0, 680), (WIDTH, 680), 2)

        charas1.update(key_lst, screen)
        charas2.update(key_lst, screen)
        beams1.update()
        beams1.draw(screen)
        beams2.update()
        beams2.draw(screen)
        exps.update()
        exps.draw(screen)
        hp_bar.update(screen)
        player1_hp.update(screen)
        player2_hp.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
