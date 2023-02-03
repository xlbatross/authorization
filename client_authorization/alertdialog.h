#ifndef ALERTDIALOG_H
#define ALERTDIALOG_H

#include <QDialog>

namespace Ui {
class AlertDialog;
}

class AlertDialog : public QDialog
{
    Q_OBJECT

public:
    explicit AlertDialog(QWidget *parent = nullptr);
    ~AlertDialog();

    void setMessage(const QString & str);

private:
    Ui::AlertDialog *ui;
};

#endif // ALERTDIALOG_H
