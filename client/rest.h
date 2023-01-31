#ifndef REST_H
#define REST_H

#include <QObject>
#include <QDebug>
#include <QEventLoop>
#include <QString>
#include <QJsonObject>
#include <QJsonDocument>
#include <QNetworkAccessManager>
#include <QNetworkReply>

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
    QByteArray container;

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

private:
    const QString baseUrl;
};

#endif // REST_H
