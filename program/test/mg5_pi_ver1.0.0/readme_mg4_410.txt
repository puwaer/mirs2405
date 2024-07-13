Ver4.0.1 README

------------------------------------------------------------
ver4.0.1との主な変更点

Makefile の変更
（本来的には gcc の記述に順番があるらしい。
　リンクするライブラリは後に持ってくる。
　以下の変更を施さないと libwiringPi に関するエラーが出る）

　変更前  $(cc) $(LDFLAGS) $^ -o $@
　変更後  $(cc) $^ -o $@ $(LDFLAGS)

OpenCV 関係の変更

  OpenCV の c++ API への書き換えに不完全な箇所があったため修正した。
  OpenCV 3 ではエラーにならなかったが OpenCV 4 系ではエラーとなるため
　修正した。（OpenCV 3 系でも問題ないことを確認している）

  get_img.cpp
  test_camera.cpp
        //cap.set(CV_CAP_PROP_FRAME_WIDTH,width);
        //cap.set(CV_CAP_PROP_FRAME_HEIGHT,height);
        cap.set(cv::CAP_PROP_FRAME_WIDTH,width);
        cap.set(cv::CAP_PROP_FRAME_HEIGHT,height);

  number_detect.cpp
        //cv::findContours(img_temp, contours, hierarchy, CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE);
        cv::findContours(img_temp, contours, hierarchy, cv::RETR_LIST, cv::CHAIN_APPROX_SIMPLE);



