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
    void emitResponse();

private slots:
    void slotFinishRequest();
    void slotReplyResponse();
    void slotReplyError();

signals:
    void responseJson(QJsonObject);
};


class AuthREST : public REST
{
public:
    AuthREST();

    void get(const QString & url);
    void classify(const cv::Mat & img);

private:
    const QString baseUrl;
};

#endif // REST_H
