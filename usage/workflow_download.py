import os
from threading import Lock

from PIL import Image

from jmcomic import *
from jmcomic.cli import JmcomicUI

# 下方填入你要下载的本子的id，一行一个，每行的首尾可以有空白字符
jm_albums = ''' 过儿童节
jm使用器
jm54747电梯（极品）
jm28650体育用具储藏室（极品）
jm27512随地小便（极品）
jm20348乡下（极品）
jm47729老师（极品）
jm61257电车（极品）
jm80358也是电车（极品）
jm18212课桌（极品）

jm488125厕所（极品）
jm485870网恋奔现纯爱
jm181611开盒主动
jm89218幼兔
jm467180永远娘（极品）
jm480142心奈小狗
jm 142464偶像堕落
jm 273943方言女孩
jm401574琴叶姐妹
jm231692小狐娘
jm306848 re：rape（极品）
jm371570 re：rape2（极品）
jm481979催眠错误
jm190447偶像大师米莉亚
jm409896桃绿
jm384297用姐姐威胁
jm485647依莉雅三人
jm495256雷电
jm271249在男厕所自被抓住了
jm74891兄妹喜欢
jm2868响
jm441594吸血鬼姐妹
jm230702妹妹想氪金
jm284185偶像大师三人
jm86779变态王子
jm478437小春
jm21994野外
jm502132制服
jm225764成为偶像
jm352727全部君
jm151696彩票
jm391894小千1
jm392101小千2
jm428347小千3
jm428348小千4
jm148624爸爸破产
jm370634七七
jm442137反催眠
jm438000反催眠2
jm467110爱玩 调教
jm145289恶毒
jm505253小凛
jm101792网购玩具
jm371631表白·主人（极品）
jm305291萝莉魅魔
jm427706被卖雌堕
jm151607妹肛
jm505048大人的游戏
jm505484雌小鬼
jm369504由美妹妹
jm501838雌小鬼糖糖
jm451610亚美全彩
jm508253两个女儿（极品）
jm355659大河（极品）
jm480841好色女孩
jm58267智绘里（童年）
jm69354面具（童年）
jm221659野外偷看
jm511010小学生女仆
jm145289恶毒
jm498750伊莉雅
jm371875雷
jm465335可可萝
jm39509大小姐宠物
jm513984离家出走少女
jm452699催眠妹妹和朋友
jm509489姬野蜜柑
jm377532幽灵先生（极品）
jm517500外卖
jm218796优妮小姐（极品）
jm481536杏（极品）
jm515569侄女
jm445794JC调教
jm248646上田裕（童年）
【Yukiu Con】 （育球康）篮球 Ganbaru！ |Givin' It My All at Basketball（童年）
jm326357 萝莉老太婆继母1 （极品）
jm241726                              2 （极品）
jm281142                              3 （极品）
jm290391                             4 （极品）
jm329995                             5 （极品）
jm429322                             日常（极品）
jm411613                               7 （极品）
jm318731                             外传（极品）

黒本君
毛玉牛乳
野际
上田裕
雪野
甘露雨

jm308472无口少女电车
jm105854纱枝
jm114445あゆみの休日はおじちゃんと…
jm98669 幼女の恩返し
jm73451三颗星彩色冒险
jm98509长度实验女孩
jm46555諏訪子さま
jm27701宅男婴儿
jm20106快递家政女孩（纯爱）
jm4333玩具被发现了
jm2388お兄ちゃんと ぺったんこ
jm122333三颗星彩色冒险
jm397150爸爸活希望碰到温柔的人
jm394523雌小鬼侄女
jm385372死库水/公主链接三人
jm362197强星宇异世界
jm346346独角兽和贝尔酱
jm305428面基男友大叔
jm2057绑架
jm333722催眠未奏希
jm220455传承优秀基因
jm148486三颗星彩色冒险
jm486253一百次才能出去的房间
jm477990幽灵女孩
jm453931强迫变成魅魔
jm452501侦探小姐被怪盗抓住了
jm343898地狱人偶有了感情
jm334554未婚妻练习
jm318730相爱才能出去的房间
jm310176占卜
jm472952百濑·和老师交往（黑本君）
jm203446亚美监禁
jm77778上班族
jm410841单亲爸爸
jm412004电车·甘露雨
jm149906球磨
jm374495魅魔和人类的女儿
jm346862学生会长
jm315728珠音和澪3
jm330006珠音和澪2
jm290455珠音和澪1
jm122427姐姐和凉酱
jm235366璃子和小田
jm265236教师拐卖
jm271249在男厕所自被抓住了
jm278032留佳·寄宿
jm487798安琪拉二次元皮cos
jm382336早柚
jm255015弟弟变成了魅魔
jm230806雌小鬼三位
jm454803偶像女儿
jm481979催眠恶作剧初中
jm434801邻居的女儿
jm434797同班女孩
jm415513催眠妹妹全彩
jm477029师生外设
jm468624圣诞小孩
jm380052偏僻乡村的女孩
jm269417两个哥哥和妹妹
jm527354芙宁娜男生推论
jm448098多娜多娜
jm509834七七cos
jm207063雌小鬼
jm293867小学毕业妹妹
jm192957 U556
jm529468可可奈的男朋友
jm209232 楽園のおもちゃ箱 5時間目
jm181107 楽園のおもちゃ箱 4時間目
jm135697 楽園のおもちゃ箱 3時間目
jm107184 楽園のおもちゃ箱 2時間目
jm127282楽園のおもちゃ箱 1 時間目
jm441189经理家的坏孩子
jm409658 替代女演员
jm116157 [雪野みなと] ものけもの
jm395281 妹妹 同学·哥哥ntr
jm395280偶像女孩经纪人
jm392326从邪魔救下夕颜酱
jm469738雌小鬼和爸爸
jm537119用涩涩照片火起来吧
jm542252 重回初中
jm62268小豆梓的变态生活
jm543247桃绿
jm368837 re：rape2（极品）
jm401496 re：rape番外
jm544360 re：rape3
jm544401 re：rape4（极品）
jm533552芙宁娜
jm549168纳西妲cos
jm471872 纳西妲cos
jm547590花神诞祭纳西妲
jm505241博士的实验纳西妲
jm392326触手纳西妲
jm476677纳西妲cos
jm223153镜华
jm21407贝蒂
jm533458胡桃催眠
jm482542风俗店胡桃
jm433023胡桃催眠
jm397478胡桃钟离
jm550176现实派蒙
jm125237仙狐
jm104738仙狐
jm293593圆角派蒙
jm303683龙王 四人和大叔
jm291407龙王 兔女郎（极品）
jm149578天衣和大叔（极品）
jm124561龙王和爱和天衣（极品）
jm78665龙王和爱和天衣（极品）
jm158龙王和爱和天衣
jm120944登山少女
jm2620六花和大叔
jm45159六花和勇太
jm13660美海 光和峰岸
jm62202美海和光
jm262147龙王的工作总集（极品）
jm551529夏洛
jm97909智花陷落
jm239027与幼女神（极品）
jm245952智花特训
jm187坏孩子美柑和家教老师
jm219坏孩子琉璃花和大叔（极品）
jm224伊莉雅催眠
jm878萝球社
jm877萝球社日向
jm759惠惠和真
jm641死库水调教1
jm610死库水调教2
jm638纱雾妖精和宗正
jm96125布のむこうがわ
jm390353下级魔法师（极品）
jm263104家教老师
jm421450小学生认身2
jm543081小学生认身1
jm484683叔侄女
jm322028厕所圣女
jm303714温泉节1
jm348168温泉节2
jm436635温泉节2.5
jm417463妈妈雌小鬼
jm245189邻家女孩
jm523276夏天要穿死库水
jm443170双胞胎时间静止
jm524360藿藿cos
jm389479猫耳前辈
jm224879妹妹发现首充
jm475378今天当个坏孩子
jm480111 u149
jm411330大河3（极品）
jm193267大河2（极品）
jm355659大河1（极品）
jm345433胡桃超度
jm278435学园孤岛银趴
jm104274小浣熊
jm435425白银和藤原·白银和辉夜
jm417420兽耳辉夜
jm275503辉夜的护身符
jm342584高木和大叔
jm320765高木和大叔
jm196775高木和西片
jm229537高木和大叔
jm85055高木和西片 仓库
jm554413惠惠和真
jm541285夜宵
jm368639丛雨
jm140620 珈百璃的堕落
jm21274天使想赚零花钱
jm20902天使和大叔
jm545733催眠天使
jm541762 BA爱莉
jm543525雌小鬼催眠老师（极品）
jm247044上田裕（童年）
jm55427银兵卫
jm251050身体偿还房租
jm220995秘密基地（极品）
jm33775万圣节收集糖（童年）
jm308595胁迫胡桃
jm306326胡桃被盗宝团抓住
jm50514少女とギャングと青い夜 （童年）（纯爱）（极品）
jm268453胡桃和小男孩
jm266615七七抓来了胡桃 和大叔
jm249121胡桃超度
jm451603智乃和哥哥
jm435777围裙智乃
jm355019大叔和智乃 催眠
jm258778兔子屋活动
jm220996牧师智乃和勇者
jm142568智乃和哥哥
jm124116拉拉队服智乃和哥哥
jm22392智乃和哥哥
jm479907纱路和大叔
jm239797纱路的香草茶
jm495051惠惠调教成功
jm501638惠惠玩具
jm398569爱丽丝
jm373099爱丽丝催眠
jm138809爱丽丝世 '''



'''

# 单独下载章节
jm_photos = '''



'''


def env(name, default, trim=('[]', '""', "''")):
    import os
    value = os.getenv(name, None)
    if value is None or value == '':
        return default

    for pair in trim:
        if value.startswith(pair[0]) and value.endswith(pair[1]):
            value = value[1:-1]

    return value


def parse_id_items(val):
    if not val:
        return set()
    if isinstance(val, (list, tuple, set)):
        res = set()
        for item in val:
            res.update(parse_id_items(str(item)))
        return res
    if not isinstance(val, str):
        val = str(val)
    res = set()
    for line in val.replace(',', '\n').splitlines():
        line = line.split('#', 1)[0].strip()
        if line:
            res.add(line)
    return res


def get_id_set(env_name, given):
    aid_set = set()
    aid_set.update(parse_id_items(given))
    env_val = env(env_name, '').replace('-', '\n')
    aid_set.update(parse_id_items(env_val))
    return aid_set


def extract_ids_from_text(source: str):
    """
    从源码文本中提取 jm_albums 和 jm_photos 的配置
    """
    import ast
    import re

    albums_str, photos_str = '', ''

    def ast_to_str(val_node):
        if val_node is None:
            return ''
        if isinstance(val_node, ast.Constant):
            return str(val_node.value)
        if isinstance(val_node, (ast.List, ast.Tuple, ast.Set)):
            return '\n'.join(str(e.value) for e in val_node.elts if isinstance(e, ast.Constant))
        return ''

    try:
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == 'jm_albums':
                            albums_str = ast_to_str(node.value)
                        elif target.id == 'jm_photos':
                            photos_str = ast_to_str(node.value)
    except Exception:
        pass

    if not albums_str:
        m = re.search(r"jm_albums\s*=\s*('''|\"\"\")(.*?)\1", source, re.DOTALL)
        if m:
            albums_str = m.group(2)
    if not photos_str:
        m = re.search(r"jm_photos\s*=\s*('''|\"\"\")(.*?)\1", source, re.DOTALL)
        if m:
            photos_str = m.group(2)

    return albums_str, photos_str


def get_id_set_from_git():
    """
    当工作区脚本被上游同步覆盖时，尝试从当前 git commit (HEAD) 自动恢复用户在 commit 中填写的 ID
    """
    import subprocess
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        res = subprocess.run(
            ['git', 'show', 'HEAD:usage/workflow_download.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            cwd=script_dir
        )
        if res.returncode == 0 and res.stdout:
            return extract_ids_from_text(res.stdout)
    except Exception:
        pass
    return '', ''


def format_file_size(size):
    if size >= 1024 * 1024:
        return f'{size / 1024 / 1024:.2f}MB'
    return f'{size / 1024:.1f}KB'


class WorkflowCompressionStats:

    def __init__(self):
        self.lock = Lock()
        self.image_count = 0
        self.original_size = 0
        self.final_size = 0

    def record(self, original_size, final_size):
        with self.lock:
            self.image_count += 1
            self.original_size += original_size
            self.final_size += final_size

    def snapshot(self):
        with self.lock:
            return self.image_count, self.original_size, self.final_size


def compress_image_in_place(filepath, quality, convert_to_jpeg=False):
    target_path = filepath
    temp_path = f'{filepath}.jmcomic-compress.tmp'
    original_size = os.path.getsize(filepath)

    try:
        with Image.open(filepath) as image:
            image_format = image.format
            image_info = image.info.copy()
            save_kwargs = {}

            if getattr(image, 'n_frames', 1) > 1:
                return image_format, None, None, False, filepath, 'multi_frame'

            if convert_to_jpeg and image_format in {'PNG', 'WEBP'}:
                image_format = 'JPEG'
                target_path = os.path.splitext(filepath)[0] + '.jpg'
                if image.mode not in {'RGB', 'L'}:
                    if image.mode in {'RGBA', 'LA'} or 'transparency' in image_info:
                        image = image.convert('RGBA')
                        background = Image.new('RGB', image.size, 'white')
                        background.paste(image, mask=image.getchannel('A'))
                        image = background
                    else:
                        image = image.convert('RGB')
                save_kwargs.update(quality=quality, optimize=True)
            elif image_format in {'JPEG', 'JPG'}:
                save_kwargs.update(quality=quality, optimize=True)
            elif image_format == 'WEBP':
                save_kwargs.update(quality=quality)
            elif image_format == 'PNG':
                return image_format, None, None, False, filepath, 'unsupported_format'
            else:
                return image_format, None, None, False, filepath, 'unsupported_format'

            for key in ('exif', 'icc_profile'):
                value = image_info.get(key)
                if value is not None:
                    save_kwargs[key] = value

            image.save(temp_path, format=image_format, **save_kwargs)

        compressed_size = os.path.getsize(temp_path)
        if target_path == filepath and compressed_size >= original_size:
            os.remove(temp_path)
            return image_format, original_size, compressed_size, False, filepath, None

        os.replace(temp_path, target_path)
        if target_path != filepath:
            os.remove(filepath)

        return image_format, original_size, compressed_size, True, target_path, None
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


class WorkflowImageCompressPlugin(JmOptionPlugin):
    plugin_key = 'workflow_image_compress'

    def invoke(self, image, quality, stats, convert_to_jpeg=False, **kwargs):
        old_path = image.save_path
        image_format, original_size, compressed_size, replaced, new_path, skip_reason = compress_image_in_place(
            old_path,
            quality,
            convert_to_jpeg,
        )

        if skip_reason == 'multi_frame':
            self.log(f'跳过多帧图片压缩以保留动画: {image_format}, {old_path}')
            return

        if original_size is None:
            self.log(f'跳过不支持质量压缩的图片格式: {image_format}, {old_path}')
            return

        if new_path != old_path:
            image.save_path = new_path

        final_size = compressed_size if replaced else original_size
        stats.record(original_size, final_size)
        compression_ratio = original_size / final_size
        action = '压缩完成' if replaced else '压缩后未变小，保留原图'
        self.log(
            f'{action}: {new_path}, '
            f'{format_file_size(original_size)} → {format_file_size(final_size)}, '
            f'压缩比 {compression_ratio:.2f}:1'
        )


class WorkflowImageCompressSummaryPlugin(JmOptionPlugin):
    plugin_key = 'workflow_image_compress_summary'

    def invoke(self, stats, **kwargs):
        image_count, original_size, final_size = stats.snapshot()
        if image_count == 0:
            self.log('压缩汇总: 没有可压缩的图片')
            return

        compression_ratio = original_size / final_size
        compression_rate = (original_size - final_size) / original_size * 100
        self.log(
            f'压缩汇总: 共处理 {image_count} 张图片, '
            f'{format_file_size(original_size)} → {format_file_size(final_size)}, '
            f'总压缩比 {compression_ratio:.2f}:1, 总压缩率 {compression_rate:.1f}%'
        )


def main():
    album_id_set = get_id_set('JM_ALBUM_IDS', jm_albums)
    photo_id_set = get_id_set('JM_PHOTO_IDS', jm_photos)

    # 兜底恢复：若本地变量与环境变量均未指定任何 ID，尝试从 git commit (HEAD) 自动恢复
    if len(album_id_set) == 0 and len(photo_id_set) == 0:
        git_albums, git_photos = get_id_set_from_git()
        if git_albums:
            album_id_set.update(parse_id_items(git_albums))
        if git_photos:
            photo_id_set.update(parse_id_items(git_photos))
        if len(album_id_set) > 0 or len(photo_id_set) > 0:
            jm_log('workflow', f'检测到工作区脚本被上游同步覆盖，已自动从 commit (HEAD) 恢复下载配置: '
                               f'album={list(album_id_set)}, photo={list(photo_id_set)}')

    # 防御性校验：若仍没有任何 ID，直接报错阻断，避免生成 247B 空压缩包误导用户
    if len(album_id_set) == 0 and len(photo_id_set) == 0:
        if env('GITHUB_REPOSITORY', '') == env('UPSTREAM_REPO', 'hect0x7/JMComic-Crawler-Python'):
            jm_log('workflow', '主仓库未配置任何本子或章节 ID，跳过下载')
            return

        ExceptionTool.raises(
            '未配置任何本子或章节 ID！请在 usage/workflow_download.py 中填写 jm_albums / jm_photos，'
            '或在 GitHub Actions 中配置环境变量 JM_ALBUM_IDS / JM_PHOTO_IDS。'
        )

    helper = JmcomicUI()
    helper.album_id_list = list(album_id_set)
    helper.photo_id_list = list(photo_id_set)

    option = get_option()
    helper.run(option)
    option.call_all_plugin('after_download')


def get_option():
    # 读取 option 配置文件
    option = create_option(os.path.abspath(os.path.join(__file__, '../../assets/option/option_workflow_download.yml')))

    # 支持工作流覆盖配置文件的配置
    cover_option_config(option)

    # 把请求错误的html下载到文件，方便GitHub Actions下载查看日志
    log_before_raise()

    return option


def cover_option_config(option: JmOption):
    dir_rule = env('DIR_RULE', None)
    if dir_rule is not None:
        the_old = option.dir_rule
        the_new = DirRule(dir_rule, base_dir=the_old.base_dir)
        option.dir_rule = the_new

    impl = env('CLIENT_IMPL', None)
    if impl is not None:
        option.client.impl = impl

    suffix = env('IMAGE_SUFFIX', None)
    if suffix is not None:
        option.download.image.suffix = fix_suffix(suffix)

    pdf_option = env('PDF_OPTION', None)
    convert_to_jpeg = bool(pdf_option and pdf_option != '否')

    try:
        image_quality = int(env('IMAGE_QUALITY', '100'))
    except ValueError:
        ExceptionTool.raises('IMAGE_QUALITY 必须是1到100之间的整数')

    ExceptionTool.require_true(
        1 <= image_quality <= 100,
        'IMAGE_QUALITY 必须是1到100之间的整数'
    )

    if image_quality < 100:
        compression_stats = WorkflowCompressionStats()
        JmModuleConfig.register_plugin(WorkflowImageCompressPlugin)
        JmModuleConfig.register_plugin(WorkflowImageCompressSummaryPlugin)
        option.plugins.setdefault('after_image', []).append({
            'plugin': WorkflowImageCompressPlugin.plugin_key,
            'kwargs': {
                'quality': image_quality,
                'convert_to_jpeg': convert_to_jpeg,
                'stats': compression_stats,
            },
        })
        option.plugins.setdefault('after_download', []).append({
            'plugin': WorkflowImageCompressSummaryPlugin.plugin_key,
            'kwargs': {
                'stats': compression_stats,
            },
        })

    if pdf_option and pdf_option != '否':
        call_when = 'after_album' if pdf_option == '是 | 本子维度合并pdf' else 'after_photo'
        
        pdf_name_rule = env('PDF_NAME_RULE', None)
        if isinstance(pdf_name_rule, str):
            pdf_name_rule = pdf_name_rule.strip()
            
        if not pdf_name_rule:
            pdf_name_rule = '[JM{Aid}] {Atitle}' if call_when == 'after_album' else '[JM{Aid}] 第{Pindex}章-JM{Pid}-{Ptitle}'
            
        plugin = [{
            'plugin': Img2pdfPlugin.plugin_key,
            'kwargs': {
                'pdf_dir': option.dir_rule.base_dir + '/pdf/',
                'filename_rule': pdf_name_rule,
                'delete_original_file': True,
            }
        }]
        option.plugins[call_when] = plugin


def log_before_raise():
    jm_download_dir = env('JM_DOWNLOAD_DIR', workspace())
    mkdir_if_not_exists(jm_download_dir)

    def decide_filepath(e):
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP, None)

        if resp is None:
            suffix = str(time_stamp())
        else:
            suffix = resp.url

        name = '-'.join(
            fix_windir_name(it)
            for it in [
                e.description,
                current_thread().name,
                suffix
            ]
        )

        path = f'{jm_download_dir}/【出错了】{name}.log'
        return path

    def exception_listener(e: JmcomicException):
        """
        异常监听器，实现了在 GitHub Actions 下，把请求错误的信息下载到文件，方便调试和通知使用者
        """
        # 决定要写入的文件路径
        path = decide_filepath(e)

        # 准备内容
        content = [
            str(type(e)),
            e.msg,
        ]
        for k, v in e.context.items():
            content.append(f'{k}: {v}')

        # resp.text
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP, None)
        if resp:
            content.append(f'响应文本: {resp.text}')

        # 写文件
        write_text(path, '\n'.join(content))

    JmModuleConfig.register_exception_listener(JmcomicException, exception_listener)


if __name__ == '__main__':
    main()
