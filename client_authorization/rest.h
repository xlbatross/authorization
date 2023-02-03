#ifndef REST_H
#define REST_H

#include <QObject>
#include <QDebug>
#include <QEventLoop>
#include <QByteArray>
#include <QString>
#include <QJsonObject>
#include <QJsonDocument>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <opencv2/opencv.hpp>

class REST : public QObject
{
    Q_OBJECT
public:
    // POST = Create, GET = Read, PUT = Update, DELETE = delete
    enum Method {POST, GET, PUT, DELETE};
    REST();
    ~REST();

    void request(int method, const QString & url, const QByteArray & rawBody = NULL);

private:
    QNetworkAccessManager * mgr;
    QNetworkReply * reply;

    qint32 statusCode;
    QString statusString;
    QString container;

    void releaseReplyResources();
    void emitCompleteResponse();

protected slots:
    void slotFinishRequest();
    void slotReplyResponse();
    void slotReplyError();

signals:
    void signalCompleteResponse(QJsonObject);
};




class AuthREST : public REST
{
    Q_OBJECT
public:
    enum ResponseType {NONE = -1, AUTHORIZATION = 1};
    AuthREST();
    void authorize(const cv::Mat & img);

private:
    const QString baseUrl;

//private slots:
//    void slotEmitResponse(QJsonObject response);

//signals:
//    void signalNoConnection();
//    void signalClassify();

};

#endif // REST_H
