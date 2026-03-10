# NFT 圖片合成器使用說明

## 快速開始

### 1. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 2. 執行程式
```bash
python nft_generator.py
```

### 3. 查看結果
生成的 NFT 圖片會儲存在 `output/` 資料夾中

## 檔案說明

- `nft_generator.py` - 主程式
- `requirements.txt` - Python 套件需求
- `Bearth_ Genesis - Metadata - Metadata (1).csv` - NFT 圖層資料
- `*.png` - 圖層圖片檔案
- `output/` - 輸出目錄（自動建立）

## 圖層疊加順序

0-BG → 1-back-back → 2-body → 3-headwear_back → 4-clothe → 5-backpack-front → 6-head → 8-emotion → 9-headwear_front → **7-holding**

（注意：7-holding 在最上層）

## 注意事項

- 如果某個圖層的值為 `0` 或 `0-0`，該圖層會被跳過
- 如果圖片檔案不存在，程式會顯示警告並繼續處理
- 程式會自動調整不同尺寸的圖片
