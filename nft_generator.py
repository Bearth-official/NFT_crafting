#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NFT 圖片合成器
根據 CSV 檔案中的圖層資訊，將 PNG 圖片依順序疊加生成 NFT 圖片
"""

import os
import pandas as pd
from PIL import Image
from pathlib import Path

# 設定路徑
BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "Bearth_ Genesis - Metadata - Metadata (3).csv"
IMAGE_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "output"

# 圖層疊加順序（注意：7-holding 在最後）
LAYER_ORDER = [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]

# 欄位名稱對應
COLUMN_NAMES = {
    0: '0-BG',
    1: '1-back-back',
    2: '2-body',
    3: '3-headwear_back',
    4: '4-clothe',
    5: '5-backpack-front',
    6: '6-head',
    7: '7-holding',
    8: '8-emotion',
    9: '9-headwear_front'
}


def load_image_with_alpha(image_path):
    """載入圖片並確保有 alpha 通道"""
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return img


def composite_images(row, image_dir):
    """
    根據 CSV 行資料合成圖片
    
    Args:
        row: pandas Series，包含圖層資訊
        image_dir: 圖片目錄路徑
    
    Returns:
        合成後的 PIL Image 物件
    """
    base_image = None
    missing_files = []
    
    for layer_index in LAYER_ORDER:
        column_name = COLUMN_NAMES[layer_index]
        layer_value = str(row[column_name]).strip()
        
        # 跳過空圖層（值為 0 或空白）
        if layer_value == '0' or layer_value == '' or layer_value == '0-0':
            continue
        
        # 建立圖片檔案路徑
        image_filename = f"{layer_value}.png"
        image_path = image_dir / image_filename
        
        # 檢查檔案是否存在
        if not image_path.exists():
            missing_files.append(image_filename)
            continue
        
        try:
            # 載入圖片
            layer_image = load_image_with_alpha(image_path)
            
            # 第一層直接設為底圖
            if base_image is None:
                base_image = layer_image
            else:
                # 確保尺寸一致
                if base_image.size != layer_image.size:
                    # 如果尺寸不同，以第一張圖的尺寸為準
                    layer_image = layer_image.resize(base_image.size, Image.LANCZOS)
                
                # 疊加圖片（保持透明度）
                base_image = Image.alpha_composite(base_image, layer_image)
        
        except Exception as e:
            print(f"  ⚠️  載入圖片失敗: {image_filename} - {e}")
            continue
    
    if missing_files:
        print(f"  ⚠️  缺少檔案: {', '.join(missing_files)}")
    
    return base_image


def main():
    """主程式"""
    print("=" * 60)
    print("NFT 圖片合成器")
    print("=" * 60)
    
    # 檢查 CSV 檔案
    if not CSV_FILE.exists():
        print(f"❌ 錯誤：找不到 CSV 檔案 {CSV_FILE}")
        return
    
    # 建立輸出目錄
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"✅ 輸出目錄：{OUTPUT_DIR}")
    
    # 讀取 CSV
    print(f"📖 讀取 CSV 檔案：{CSV_FILE.name}")
    df = pd.read_csv(CSV_FILE)
    total_count = len(df)
    print(f"✅ 共 {total_count} 筆資料")
    
    # 處理每一筆資料
    print("\n開始處理...")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    
    for index, row in df.iterrows():
        nft_num = row['int_num']
        output_filename = f"{nft_num}.png"
        output_path = OUTPUT_DIR / output_filename
        
        # 顯示進度
        progress = index + 1
        print(f"\n[{progress}/{total_count}] 處理中: {nft_num}")
        
        try:
            # 合成圖片
            composite_image = composite_images(row, IMAGE_DIR)
            
            if composite_image is None:
                print(f"  ❌ 失敗：無法生成圖片（可能所有圖層都缺失）")
                error_count += 1
                continue
            
            # 儲存圖片
            composite_image.save(output_path, 'PNG')
            print(f"  ✅ 已儲存: {output_filename}")
            success_count += 1
        
        except Exception as e:
            print(f"  ❌ 錯誤: {e}")
            error_count += 1
    
    # 顯示統計
    print("\n" + "=" * 60)
    print("處理完成！")
    print("-" * 60)
    print(f"✅ 成功: {success_count} 張")
    print(f"❌ 失敗: {error_count} 張")
    print(f"📁 輸出位置: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
