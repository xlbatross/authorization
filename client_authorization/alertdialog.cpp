#include "alertdialog.h"
#include "ui_alertdialog.h"

AlertDialog::AlertDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::AlertDialog)
{
    ui->setupUi(this);

    this->setWindowFlags(Qt::Dialog | Qt::WindowTitleHint);
}

AlertDialog::~AlertDialog()
{
    delete ui;
}

void AlertDialog::setMessage(const QString &str)
{
    ui->lbl_msg->setText(str);
}
