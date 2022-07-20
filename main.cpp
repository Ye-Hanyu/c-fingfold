#include <stdio.h>
#include <iostream>
#include <string>
#include "cc_util.hpp"
#include <opencv2/opencv.hpp>
int main(int argc, char *argv[])
{
    using namespace cv;
    using namespace std;
    for(int i=0; i<argc; i++){
        cout << argv[i] << "  ";
         }



cout << "begin end ha" << endl;

#if defined(__linux__)
	cout << "__linux__ is defined as " << __linux__ << endl;
    cout << LINFO << endl;

    // Mat img = imread("/home/ye/图片/图片1.png");
	// imshow("Image", img);//创建一个窗口来显示图像img
	// waitKey(0);//不断刷新图像
    HelloFunc();
    string str1="hahs.png";
    string str2="hahs.png;hahs.png";
    const char *srt1 = str1.c_str();
    const char *srt2 = str2.c_str();
    bool is_same = ccutil::patternMatch(srt1, srt2);
    ccutil::BBox btest2 ={56.2,24.3,45.6,45.1,99.9,1} ;
    ccutil::BBox btest = {};
    string filter = "*";
    vector<string> list = ccutil::findFiles("/home/ye/图片", filter, true, true);
    string file = "/home/ye/图片/test.xml";
    string data = ccutil::loadfile(file);
    auto size = ccutil::fileSize(file);
    int width = 1344;

    vector<ccutil::LabBBox> box = ccutil::loadxmlFromData(data, &width, &width, filter);
    string file2 = "/home/ye/图片/test2.xml";
    string imagename = "test.jpg";
    ccutil::savexml(file2, imagename, width, width, box);
    string file3 = "/home/ye/图片/test.txt";
    ccutil::saveList(file3, list);
    vector<string> list_s = ccutil::loadList(file3);
    // for (int i=0;i<list.size();i++){
    // Mat img = imread(list[i]);
    // namedWindow("window",cv::WINDOW_NORMAL);
    // resizeWindow("window",cv::Size(640*2,480*2));
	// imshow("window", img);//创建一个窗口来显示图像img
	// waitKey(2000);//不断刷新图像
    // }
#else
    cout << "linux" << endl;
    cout << "good" << endl;
#endif
 

    return 0;

}