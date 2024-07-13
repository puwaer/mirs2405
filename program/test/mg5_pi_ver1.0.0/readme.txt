mg5_rp4_be_ver 11.0.0

------------------------------------------------------------
MG5のRaspberry Pi の標準プログラム
ハードウェア　Raspberry Pi 4
OS: Bullseye (32 bit/64bit)

概要
・mg4_pi_ver4.1.0 をベースにしている
・Bullseue では、 WiringPi と OpenCV C++ をソースからコンパイル・インストール
する必要があった。
  インストールバージョン
    WiringPi 2.7
    OpenCV 4.9

  WirngPi のインストール
	https://qiita.com/tamamori/items/f40d7d81111a91354220	
  OpenCV C++ のインストール
	https://www.koi.mashykom.com/Raspi_opencv.html#fd03	

mg4_pi_ver4.1.0 からの変更点

1. Makefile のコンパイルオプションで opecv を opecv4 とした
2. src/pilot.c の Warning をなくした（double volt をコメントアウトした）
3. src/cicle_ditect.c と src/color_binarize.c を削除した





