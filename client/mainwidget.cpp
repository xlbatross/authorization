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
    , alertDialog(new AlertDialog(this))
{
    ui->setupUi(this);

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    ui->lbl_loading->setMovie(mv_loading);
    ui->lbl_loading->setVisible(false);

    captureTimer->setInterval(33);
    clearTimer->setInterval(1500);

    connect(ui->btn, SIGNAL(clicked(bool)), this, SLOT(slotSendRequest()));
    connect(authRest, SIGNAL(signalCompleteResponse(QJsonObject)), this, SLOT(slotResponse(QJsonObject)));
    connect(captureTimer, SIGNAL(timeout()), this, SLOT(slotCaptureVideo()));
    connect(clearTimer, SIGNAL(timeout()), this, SLOT(slotClearState()));

    captureTimer->start();
    slotCaptureVideo();
}

MainWidget::~MainWidget()
{
    delete ui;
    delete authRest;
    delete mv_loading;
    delete captureTimer;
    delete clearTimer;
    delete alertDialog;
}

void MainWidget::slotCaptureVideo()
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

void MainWidget::slotSendRequest()
{
    mv_loading->start();
    ui->lbl_loading->setVisible(true);

    ui->btn->setEnabled(false);
    captureTimer->stop();

    imgMutex.lock();
    authRest->classify(img);
    imgMutex.unlock();
}

void MainWidget::slotResponse(QJsonObject response)
{
    mv_loading->stop();
    ui->lbl_loading->setVisible(false);

    int statusCode = response["statusCode"].toInt();

    if (statusCode >= 300 || statusCode < 200)
    {
        alertDialog->setMessage(response["statusString"].toString());
    }
    else
    {
        QJsonObject body = response["body"].toObject();
        int type = body["type"].toInt();
        QJsonObject attribute = body["attribute"].toObject();

        switch(type)
        {
        case NONE:
            alertDialog->setMessage("잘못된 데이터가 전송되었습니다.");
            break;
        case CLASSIFY:
        {
            if(attribute.keys().contains("image"))
            {
                QByteArray utf8decoding = attribute["image"].toString().toUtf8();
                QByteArray base64Decoding = QByteArray::fromBase64(utf8decoding);

                imgMutex.lock();
                cv::Mat m(480, 640, CV_8UC3, base64Decoding.data());
                QImage qtImage(m.data, m.cols, m.rows, QImage::Format_RGB888);
                QPixmap qtPixmap = QPixmap::fromImage(qtImage);
                ui->lbl_image->setPixmap(qtPixmap);
                imgMutex.unlock();

                alertDialog->setMessage("OOO씨\n어서오세요");
            }
        } break;
        }
    }

    clearTimer->start();
    alertDialog->exec();
}

void MainWidget::slotClearState()
{
    if (clearTimer->isActive())
        clearTimer->stop();
    alertDialog->close();

    ui->btn->setEnabled(true);
    captureTimer->start();
}

