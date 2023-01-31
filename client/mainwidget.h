#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include <QWidget>
#include <QMovie>
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
    Ui::MainWidget *ui;
    AuthREST * authRest;

    QMovie * loading;

private slots:
    void sendRequest();
    void responseJson(QJsonObject response);
};
#endif // MAINWIDGET_H
