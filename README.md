# Octoprint Case Control
 A simple plugin for Octoprint which allows for relay control of a printer using the sever webpage or a physical button. There are three buttons on the case, the first turns off the raspberry pi server, the second turns the printer on and off, and the last button has been unassigned. The server webpage has a new icon in the navbar which allows for remote control of the printers power.
 ![OctoprintPage](https://user-images.githubusercontent.com/85288181/121022194-16412500-c7dd-11eb-98fa-f162acf11281.png)
 
 Look in this repository for GIFs showing the power toggling in action.

３Ｄプリンターの自動化。もっと手間を抜くため、LANで３Ｄプリンターを作動したかった。作動するため、ラズパイのStretchに基づいてのOctoprintっていうOSにした。USBケーブルでラズパイが３Ｄプリンターに繋ぎ、OctoprintのWeb serverのおかげでweb browserがあるデバイスで３Ｄプリンターを作動できる。Octoprintでネットワークに繋いでるデバイスでファイルをアップしたり、印刷をはじまれたりすることできます。しかし、３Ｄプリンターの電源の制御も欲しかったから、Octoprintのユーザーインターフェースに繋いでるPythonスクリプト書いた。雷の文字のボックスをクリックすると、電源がOn/Offになる。プリンターの電源切るため、ACアダプターへの配線を切れるリレーにした。このリレーはラズパイのGPIOに制御されている。印刷終えた後に３Ｄプリンターの電源切る時は、print headが冷やさないうちに電源切ったら害になるので、３Ｄプリンターから
温度のデータ読み込んで切れるかどうか判断できる。その上、印刷中の時も電源を切れない。
