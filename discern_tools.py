import logging

from PIL import Image, ImageFilter
import imagehash


def same_pos_picture():
    img = Image.open("input2.png")

    scale = 1.5
    wechat_width = 150 * scale
    wechat_height = 30 * scale
    wechat_x = 400 * scale
    wechat_y = 20 * scale

    crop_x, crop_y = wechat_x + 10, wechat_y
    crop_width, crop_height = wechat_width - 20, wechat_height
    crop_box = (crop_x, crop_y, crop_x + crop_width, crop_y + crop_height)
    cropped = img.crop(crop_box)

    img1 = Image.open("anchor_point/img_1.png").convert("RGB")
    img2 = cropped.convert("RGB")


    # 计算感知哈希（phash对缩放和轻微变形最鲁棒）
    hash1 = imagehash.phash(img1, hash_size=16)  # 加大hash_size提升精度
    hash2 = imagehash.phash(img2, hash_size=16)

    distance = hash1 - hash2
    max_dist = 16 * 16
    similarity = (1 - distance / max_dist) * 100

    logging.debug(f"哈希距离: {distance}")
    logging.debug(f"相似度: {similarity:.1f}%")

    if distance <= 6:
        return True
    else:
        return False


if __name__ == '__main__':
    print(same_pos_picture())
