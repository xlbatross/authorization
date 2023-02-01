#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include <QWidget>
#include <QMutex>
#include <QTimer>
#include <QImage>
#include <QMovie>
#include <QMessageBox>
#include <opencv2/opencv.hpp>
#include "rest.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWidget; }
QT_END_NAMESPACE

class MainWidget : public QWidget
{
    Q_OBJECT

public:
    MainWidget(QWidget *parent = nullptr);
    ~MainWidget();

private:
    AuthREST * authRest;

    cv::VideoCapture cap;
    cv::Mat img;

    Ui::MainWidget *ui;

    QMovie * mv_loading;
    QTimer * captureTimer;
    QTimer * clearTimer;
    QMutex imgMutex;

private slots:
    void captureVideo();
    void sendRequest();
    void responseJson(QJsonObject response);
    void clearState();
};
#endif // MAINWIDGET_H
