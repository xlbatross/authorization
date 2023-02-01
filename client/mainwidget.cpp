#include "mainwidget.h"
#include "./ui_mainwidget.h"

MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
    , authRest(new AuthREST)
    , cap(0)
    , ui(new Ui::MainWidget)
    , mv_loading(new QMovie(":/gif/resource/Spinner-1s-200px.gif"))
    , captureTimer(new QTimer(this))
    , clearTimer(new QTimer(this))
{
    ui->setupUi(this);

    ui->lbl_loading->setMovie(mv_loading);
    ui->lbl_loading->setVisible(false);

    captureTimer->setInterval(33);
    clearTimer->setInterval(1500);

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    connect(ui->btn, SIGNAL(clicked(bool)), this, SLOT(sendRequest()));
    connect(authRest, SIGNAL(responseJson(QJsonObject)), this, SLOT(responseJson(QJsonObject)));
    connect(captureTimer, SIGNAL(timeout()), this, SLOT(captureVideo()));
    connect(clearTimer, SIGNAL(timeout()), this, SLOT(clearState()));

    captureTimer->start();
    captureVideo();
}

MainWidget::~MainWidget()
{
    delete ui;
    delete authRest;
    delete mv_loading;
    delete captureTimer;
    delete clearTimer;
}

void MainWidget::captureVideo()
{
    imgMutex.lock();
    if(captureTimer->isActive() && cap.read(img))
    {
        cv::cvtColor(img, img, cv::COLOR_BGR2RGB);
        QImage qtImage(img.data, img.cols, img.rows, QImage::Format_RGB888);
        QPixmap qtPixmap = QPixmap::fromImage(qtImage);
        ui->lbl_image->setPixmap(qtPixmap);
    }
    imgMutex.unlock();
}

void MainWidget::sendRequest()
{
    mv_loading->start();
    ui->lbl_loading->setVisible(true);

    ui->btn->setEnabled(false);
    captureTimer->stop();

    imgMutex.lock();
    authRest->classify(img);
    imgMutex.unlock();
}

void MainWidget::responseJson(QJsonObject response)
{
    mv_loading->stop();
    ui->lbl_loading->setVisible(false);

    QJsonObject body = response["body"].toObject();

    if(body.keys().contains("image"))
    {
        QByteArray utf8decoding = body["image"].toString().toUtf8();
        QByteArray base64Decoding = QByteArray::fromBase64(utf8decoding);

        imgMutex.lock();
        cv::Mat m(480, 640, CV_8UC3, base64Decoding.data());
        QImage qtImage(m.data, m.cols, m.rows, QImage::Format_RGB888);
        QPixmap qtPixmap = QPixmap::fromImage(qtImage);
        ui->lbl_image->setPixmap(qtPixmap);
        imgMutex.unlock();
    }

    clearTimer->start();
}

void MainWidget::clearState()
{
    clearTimer->stop();

    ui->btn->setEnabled(true);
    captureTimer->start();
}

