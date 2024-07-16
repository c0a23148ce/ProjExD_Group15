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
        
class Skill_cut_1(pg.sprite.Sprite):
    """
    キャラに対応したスキルを発動
    """
    def __init__(self, life, num, screen: pg.Surface):
        super().__init__()
        self.life = life
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        pg.draw.rect(self.image, (0, 0, 0), (WIDTH/2, 0, 290, 190))
        pg.draw.polygon(self.image, (255,255,255), [[630, 220], [865, 160], [900, 165], [935, 145], [WIDTH, 110],[WIDTH,260], [1050, 250], [970, 280], [630, 295], [500,280]]) 
        pg.draw.polygon(self.image, (0,0,255), [[630, 230], [865, 170], [900, 175], [935, 155], [WIDTH, 120],[WIDTH,240], [1050, 240], [970, 270], [630, 285], [530,275]])       
        #pg.draw.rect(self.image, (0, 0, 0), (WIDTH/2, 0, 290, 190))
        #pg.draw.rect(self.image, (0, 0, 255), (WIDTH/2, 0, 270, 170))
        self.image.set_alpha(200)
        self.image_cut = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 5)
        self.rect_cut = self.image_cut.get_rect()

    def update(self, screen):
        self.life -= 1
        screen.blit(self.image_cut, (WIDTH*5/7, HEIGHT*2/9))
        if self.life < 0:
            self.kill()
        if check_bound(self.rect) != (True, True):
            self.kill()

class Skill_1(pg.sprite.Sprite):
    """
    キャラクター１のスキルに関するクラス
    """
    def __init__(self, chara: Chara_1):
        """
        スキル画像Surfaceを生成する
        引数 chara_1：スキルを放つキャラクター
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
        self.speed = 100

    def update(self):
        """
        スキルを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(self.speed*self.vx, self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()

class Skillpoint_1:
    """
    時間経過と共に上昇するスキルポイント
    """
    def __init__(self):
        self.value = 0
        self.gauge_img0_1 = pg.transform.rotozoom(pg.image.load(f"fig/{3}.png"), 0, 1)

    def update(self):
        if (self.value < 100):
            self.value += 0.25

    def draw_gauge(self, surface, x, y, radius_1, current_1, maximum_1):

        # ゲージの背景（白で円を描画）
        pg.draw.circle(surface, (255, 255, 255), (x, y), radius_1)

        # 充填部分（青で扇形を描画）
        angle_1 = (current_1 / maximum_1) * 360  # 充填率を角度に変換
        start_angle_1 = 90  #90度から描画する
        end_angle_1 = start_angle_1 + 270/360 * angle_1
        pg.draw.arc(surface, (0, 0, 255), (x - radius_1, y - radius_1, 2 * radius_1, 2 * radius_1), math.radians(start_angle_1), math.radians(end_angle_1), width=radius_1)
        pg.draw.circle(surface, (0, 0, 0), (x, y), radius_1/2)
        pg.draw.rect(surface, (0, 0, 0), (x, y - radius_1, radius_1, radius_1))
        surface.blit(self.gauge_img0_1, (x, y - radius_1))

class Skill_cut_2(pg.sprite.Sprite):
    """
    キャラに対応したスキルを発動
    """
    def __init__(self, life, num, screen: pg.Surface):
        super().__init__()
        self.life = life
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        pg.draw.rect(self.image, (0, 0, 0), (WIDTH/2, 0, 290, 190))
        pg.draw.polygon(self.image, (255,255,255), [[630, 220], [865, 160], [900, 165], [935, 145], [WIDTH, 110],[WIDTH,260], [1050, 250], [970, 280], [630, 295], [500,280]]) 
        pg.draw.polygon(self.image, (0,0,255), [[630, 230], [865, 170], [900, 175], [935, 155], [WIDTH, 120],[WIDTH,240], [1050, 240], [970, 270], [630, 285], [530,275]])       
        #pg.draw.rect(self.image, (0, 0, 0), (WIDTH/2, 0, 290, 190))
        #pg.draw.rect(self.image, (0, 0, 255), (WIDTH/2, 0, 270, 170))
        self.image.set_alpha(200)
        self.image_cut = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 5)
        self.rect_cut = self.image_cut.get_rect()

    def update(self, screen):
        self.life -= 1
        screen.blit(self.image_cut, (WIDTH*5/7, HEIGHT*2/9))
        if self.life < 0:
            self.kill()
        if check_bound(self.rect) != (True, True):
            self.kill()

class Skill_2(pg.sprite.Sprite):
    """
    キャラクター１のスキルに関するクラス
    """
    def __init__(self, chara: Chara_2):
        """
        スキル画像Surfaceを生成する
        引数 chara_2：スキルを放つキャラクター
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
        self.speed = 100

    def update(self):
        """
        スキルを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(self.speed*self.vx, self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()

class Skillpoint_2:
    """
    時間経過と共に上昇するスキルポイント
    """
    def __init__(self):
        self.value = 0
        self.gauge_img0_2 = pg.transform.rotozoom(pg.image.load(f"fig/{32}.png"), 0, 1)

    def update(self):
        if (self.value < 100):
            self.value += 0.25

    def draw_gauge(self, surface, x, y, radius_2, current_2, maximum_2):

        # ゲージの背景（白で円を描画）
        pg.draw.circle(surface, (255, 255, 255), (x, y), radius_2)

        # 充填部分（青で扇形を描画）
        angle_2 = (current_2 / maximum_2) * 360  # 充填率を角度に変換
        start_angle_2 = 90  #90度から描画する
        end_angle_2 = start_angle_2 + 270/360 * angle_2
        pg.draw.arc(surface, (0, 0, 255), (x - radius_2, y - radius_2, 2 * radius_2, 2 * radius_2), math.radians(start_angle_2), math.radians(end_angle_2), width=radius_2)
        pg.draw.circle(surface, (0, 0, 0), (x, y), radius_2/2)
        pg.draw.rect(surface, (0, 0, 0), (x, y - radius_2, radius_2, radius_2))
        surface.blit(self.gauge_img0_2, (x, y - radius_2))

def main():
    pg.display.set_caption("HADOU!!こうかとん!!")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"fig/background.jpg")

    charas1 = Chara_1(3, (WIDTH*3/4+20, HEIGHT/2+50))
    charas2 = Chara_2(32, (WIDTH/4-35, HEIGHT/2+45))
    beams1 = pg.sprite.Group()
    beams2 = pg.sprite.Group()
    exps = pg.sprite.Group()
    skill1 = pg.sprite.Group()
    skill2 = pg.sprite.Group()

    skillpoint1 = Skillpoint_1()
    skill_gauge_value_1 = 0
    max_value_1 = 100
    skillpoint2 = Skillpoint_2()
    skill_gauge_value_2 = 0
    max_value_2 = 100


    tmr = 0
    clock = pg.time.Clock()
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
            exps.add(Explosion(charas1, 100))  # 爆発エフェクト
            charas2.change_img(62, screen)  # こうかとん喜びエフェクト
            charas1.change_img(8, screen) # こうかとん悲しみエフェクト
            pg.display.update()
            time.sleep(2)
            return
        
        # chara2とビームの当たり判定
        if len(pg.sprite.spritecollide(charas2, beams1, True)) != 0:
            exps.add(Explosion(charas2, 100))  # 爆発エフェクト
            charas1.change_img(6, screen)  # こうかとん喜びエフェクト
            charas2.change_img(82, screen) # こうかとん悲しみエフェクト
            pg.display.update()
            time.sleep(2)
            return

        #chara1の必殺技
        if skill_gauge_value_1 == 100 and event.type == pg.KEYDOWN and event.key == pg.K_RCTRL:
            #skill.add(Skill_1(35, 300, screen))
            skill1.add(Skill_1(charas1))# スキル発射！
            skill_gauge_value_1 = 0
        
        #ゲージの変化
        if skill_gauge_value_1 != max_value_1: # ゲージを増やす
            skill_gauge_value_1 += 0.25

        # chara2とchara1スキルの当たり判定
        if len(pg.sprite.spritecollide(charas2, skill1, True)) != 0:
            exps.add(Explosion(charas2, 100))  # 爆発エフェクト
            charas1.change_img(6, screen)  # こうかとん喜びエフェクト
            charas2.change_img(82, screen) # こうかとん悲しみエフェクト
            pg.display.update()
            time.sleep(2)
            return
        
        #chara2の必殺技
        if skill_gauge_value_2 == 100 and event.type == pg.KEYDOWN and event.key == pg.K_LCTRL:
            #skill.add(Skill_2(35, 300, screen))
            skill2.add(Skill_2(charas2))# スキル発射！
            skill_gauge_value_2 = 0
        
        #ゲージの変化
        if skill_gauge_value_2 != max_value_2: # ゲージを増やす
            skill_gauge_value_2 += 0.25

        # chara1とchara2スキルの当たり判定
        if len(pg.sprite.spritecollide(charas1, skill2, True)) != 0:
            exps.add(Explosion(charas1, 100))  # 爆発エフェクト
            charas2.change_img(6, screen)  # こうかとん喜びエフェクト
            charas1.change_img(82, screen) # こうかとん悲しみエフェクト
            pg.display.update()
            time.sleep(2)
            return


        # 座標確認用(座標を確認したいときに使ってね！)
        #line = pg.Surface((WIDTH, HEIGHT))
        #pg.draw.line(screen, (255, 0, 0), (0, 680), (WIDTH, 680), 2)

        charas1.update(key_lst, screen)
        charas2.update(key_lst, screen)
        beams1.update()
        beams1.draw(screen)
        beams2.update()
        beams2.draw(screen)
        exps.update()
        exps.draw(screen)
        skillpoint1.draw_gauge(screen, WIDTH -50, 70, 50, skill_gauge_value_1, max_value_1)
        skill1.update()
        skill1.draw(screen)
        skillpoint2.draw_gauge(screen, 50, 70, 50, skill_gauge_value_2, max_value_2)
        skill2.update()
        skill2.draw(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
