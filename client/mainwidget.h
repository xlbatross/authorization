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
#include "alertdialog.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWidget; }
QT_END_NAMESPACE

class MainWidget : public QWidget
{
    Q_OBJECT

public:
    enum ResponseType {NONE = -1, CLASSIFY = 1};
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
    AlertDialog * alertDialog;
    QMutex imgMutex;

private slots:
    void slotSendRequest();
    void slotResponse(QJsonObject response);
    void slotCaptureVideo();
    void slotClearState();
};
#endif // MAINWIDGET_H
