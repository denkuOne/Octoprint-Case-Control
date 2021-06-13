# Octoprint Case Control

下に日本語の説明あります。

 A simple plugin for Octoprint which allows for relay control of a printer using the sever webpage or a physical button. There are three buttons on the case, the first turns off the raspberry pi server, the second turns the printer on and off, and the last button has been unassigned. The server webpage has a new icon in the navbar which allows for remote control of the printers power.
![OctoprintPage](https://user-images.githubusercontent.com/85288181/121022814-a7b09700-c7dd-11eb-88b8-2406aac6110a.png) 
 Look in this repository for GIFs showing the power toggling in action.

# 説明
３Ｄプリンターの自動化のプロジェクトです。手間を省くため、LANで３Ｄプリンターを作動しました。作動するため、ラズパイのStretchに基づいてのOctoprintというOSにしました。USBケーブルでラズパイを３Ｄプリンターに繋ぎ、Octoprintのサーバーのおかげでブラウザがあるデバイスで３Ｄプリンターを作動できます。Octoprintでネットワークに繋いでるデバイスでファイルをアップしたり、印刷をはじめたりすることができます。しかし、３Ｄプリンターの電源の制御も欲しかったので、Octoprintのユーザーインターフェースに繋いでるPythonスクリプトを書きました。上にある雷のアイコンをクリックすると、電源がOn/Offになります。プリンターの電源を切るため、ACアダプターへの配線を切れるリレーにしました。このリレーはラズパイのGPIOで制御されています。印刷が終わった時、ホットエンド・ノズルが熱いまま、電源を切ったら故障の原因になるので、３Ｄプリンターから温度のデータを読み込んで電源を切っていいかどうか判断できます。その上、印刷中も電源が切れることはありません。
