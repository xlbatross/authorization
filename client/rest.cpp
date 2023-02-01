#include "rest.h"

REST::REST()
{
    mgr = new QNetworkAccessManager(this);
}

REST::~REST()
{
    delete mgr;
}

void REST::request(int method, const QString & url, const QByteArray & rawBody)
{
    container.clear();

    QUrl urlObject(url);
    QNetworkRequest request(urlObject);

    switch(method)
    {
    case POST:
    {
        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
        reply = mgr->post(request, rawBody);
    }   break;
    case GET:
        reply = mgr->get(request);
        break;
    case PUT:
    {
        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
        reply = mgr->put(request, rawBody);
    }   break;
    case DELETE :
        reply = mgr->deleteResource(request);
        break;
    default:
        break; // error
    }

    connect(reply, SIGNAL(readyRead()), SLOT(slotReplyResponse()));
    connect(reply, SIGNAL(error(QNetworkReply::NetworkError)), SLOT(slotReplyError()));
    connect(reply, SIGNAL(finished()), SLOT(slotFinishRequest()));
}

void REST::releaseReplyResources()
{
    disconnect(reply, SIGNAL(readyRead()), this, SLOT(slotReplyResponse()));
    disconnect(reply, SIGNAL(error(QNetworkReply::NetworkError)), this,SLOT(slotReplyError()));
    disconnect(reply, SIGNAL(finished()), this, SLOT(slotFinishRequest()));

    reply->deleteLater();
}

void REST::emitResponse()
{
    QVariant status_code = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute);
    if (status_code.isValid())
    {
        statusCode = status_code.toInt();
    }
    else
    {
        statusCode = -1;
    }

    QJsonObject body = QJsonDocument::fromJson(container.toUtf8()).object();

    QJsonObject response;
    response["statusCode"] = statusCode;
    response["statusString"] = statusString;
    response["body"] = body;

    emit responseJson(response);
}

void REST::slotReplyResponse()
{
    container.append(reply->readAll());
}

void REST::slotReplyError()
{
    statusString = reply->errorString();
    releaseReplyResources();
    emitResponse();
}

void REST::slotFinishRequest()
{
    statusString = "OK";
    releaseReplyResources();
    emitResponse();
}





AuthREST::AuthREST()
    : REST()
    , baseUrl("http://127.0.0.1:5000")
{

}

void AuthREST::get(const QString & url)
{
    request(REST::GET, baseUrl + url);
}

void AuthREST::classify(const cv::Mat &img)
{
    // base64로 인코딩 -> utf-8로 디코딩
    QByteArray base64encoding = QByteArray((char *)img.data, img.total() * img.channels()).toBase64();
    QString utf8decoding = QString::fromUtf8(base64encoding);

    QJsonObject body;
    body["image"] = utf8decoding;

    QJsonDocument doc;
    doc.setObject(body);

    request(REST::POST, baseUrl + "/classify", doc.toJson());
}


