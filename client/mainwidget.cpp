#include "mainwidget.h"
#include "./ui_mainwidget.h"

MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MainWidget)
    , authRest(new AuthREST)
    , loading(new QMovie(":/gif/resource/Spinner-1s-200px.gif"))
{
    ui->setupUi(this);

    connect(ui->btn, SIGNAL(clicked(bool)), this, SLOT(sendRequest()));
    connect(authRest, SIGNAL(responseJson(QJsonObject)), this, SLOT(responseJson(QJsonObject)));
}

MainWidget::~MainWidget()
{
    delete ui;
    delete authRest;
    delete loading;
}

void MainWidget::sendRequest()
{
    ui->label->setMovie(loading);
    loading->start();
    ui->btn->setEnabled(false);

    authRest->get("/hello");
}

void MainWidget::responseJson(QJsonObject response)
{
    qDebug() << response;
    qDebug() << response["body"].toObject();

    ui->label->clear();
    loading->stop();
    ui->btn->setEnabled(true);
}

