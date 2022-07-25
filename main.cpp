/*** 
 * @Author: YeHanyu
 * @Date: 2022-07-18 11:47:53
 * @LastEditors: YeHanyu
 * @LastEditTime: 2022-07-25 14:31:49
 * @FilePath: /c-fingfold/main.cpp
 * @Description: 
 * @
 * @Copyright (c) 2022 by YeHanyu, All Rights Reserved. 
 */
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
    // HelloFunc();
    // ccutil::BBox btest3 ={0,0,200,100,99.9,1} ;
    // const cv::Size size1(450,450);
    // ccutil::BBox btest4=btest3.expand(2);
    // const string file = "/home/ye/图片/test.xml";
    // string file_data = ccutil::loadfile(file);
    // string *file_ptr = &file_data;
    // const string mode = "rw";
    // ccutil::BinIO bino = ccutil::BinIO(file_ptr);
    // int length = 0;
    // bino >> length;
    
    // // bino.openMemoryWrite();
    // char data_bino[5]="abcd";
    // bino << data_bino;


    // int info[4];
    string str1="asdf.png";
    // auto val = ccutil::S(str1)(0, -3);
    string str2="hahs.png;asdf.png";
    string str3 = "s";
    vector<string> vstr;
    vstr = ccutil::split(str2, str3);
    // string dir = "/home/ye/图片/1";
    // bool is_dir = ccutil::rmtree(dir);
    const char *srt1 = str1.c_str();
    const char *srt2 = str2.c_str();
    bool is_same = ccutil::patternMatch(srt1, srt2);
    // ccutil::BBox btest2 ={200,200,600,600,99.9,1} ;
    // string imgf = "/home/ye/图片/test.png";
    // Mat img = imread(imgf);
    // ccutil::drawbbox(img, btest2, ccutil::Voc, str1);
    // namedWindow("window",cv::WINDOW_NORMAL);
    // resizeWindow("window",cv::Size(640*2,480*2));
	// imshow("window", img);//创建一个窗口来显示图像img
	// waitKey(0);//不断刷新图像
    // ccutil::BBox btest = {};
    // string filter = "*";
    // vector<string> list = ccutil::findFiles("/home/ye/图片", filter, true, true);
    // ;
    // string data = ccutil::loadfile(file);
    // auto size = ccutil::fileSize(file);
    // int width = 1344;

    // vector<ccutil::LabBBox> box = ccutil::loadxmlFromData(data, &width, &width, filter);
    // string file2 = "/home/ye/图片/test2.xml";
    // string imagename = "test.jpg";
    // ccutil::savexml(file2, imagename, width, width, box);
    // string file3 = "/home/ye/图片/test.txt";
    // ccutil::saveList(file3, list);
    // vector<string> list_s = ccutil::loadList(file3);
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