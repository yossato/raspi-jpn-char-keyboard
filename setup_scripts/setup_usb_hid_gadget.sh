#!/bin/bash

GADGET_DIR=/sys/kernel/config/usb_gadget/composite_gadget

# libcompositeモジュールのロード
modprobe libcomposite

# USBガジェットディレクトリ作成
mkdir -p $GADGET_DIR
cd $GADGET_DIR || exit

# デバイス設定
echo 0x1d6b > idVendor  # Linux Foundation
echo 0x0104 > idProduct # Composite Gadget
echo 0x0100 > bcdDevice # バージョン番号
echo 0x0200 > bcdUSB    # USB 2.0

# 言語と製造元情報設定
mkdir -p strings/0x409
echo "1234567890" > strings/0x409/serialnumber
echo "My Manufacturer" > strings/0x409/manufacturer
echo "Composite HID & Audio & Serial" > strings/0x409/product

# Configurationの設定
mkdir -p configs/c.1/strings/0x409
echo "Composite Config" > configs/c.1/strings/0x409/configuration
echo 120 > configs/c.1/MaxPower

# HID設定
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/

# USBコントローラのバインド
echo "$(ls /sys/class/udc)" > UDC

chmod 666 /dev/hidg0