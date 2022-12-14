from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np
from our_library.tools import binary_accuracy, multi_class_f1


class Wrapper:
    def __init__(
        self,
        model,
        loss,
        learning_rate=0.001,
        multi_class=False,
        custom_metric_function=None,
        verbose=True,
    ):

        self.model = model
        self.loss = loss
        self.learning_rate = learning_rate

        self.multi_class = multi_class

        self.metric_function = custom_metric_function or (
            binary_accuracy if not self.multi_class else multi_class_f1
        )

        self.verbose = verbose

        self.losses = []
        self.losses_per_epoch = []

        self.metric = []
        self.metric_per_epoch = []
        self.metric_per_epoch_test = []

    def train(self, train_loader, test_loader, epochs=15):

        progress_bar = None

        try:

            for n_epoch in range(epochs):

                epoch_losses = []
                epoch_metric = []
                epoch_metric_test = []

                progress_bar = tqdm(
                    total=len(train_loader),
                    desc="Epoch {}".format(n_epoch + 1), disable=not self.verbose
                )

                for batch in train_loader:

                    x, y = self.batch_processing(batch)

                    loss_batch, prediction = self.train_batch(x, y)

                    self.losses.append(loss_batch)
                    epoch_losses.append(loss_batch)
                    
                    batch_metric = self.metric_function(y, prediction)

                    self.metric.append(batch_metric)
                    epoch_metric.append(batch_metric)

                    progress_bar.update()

                    progress_bar.set_postfix(loss=np.mean(epoch_losses), metric=np.mean(epoch_metric))

                for batch in test_loader:

                    x, y = self.batch_processing(batch)
                    prediction = self.predict_batch(x)

                    batch_accuracy = self.metric_function(y, prediction)

                    epoch_metric_test.append(np.mean(batch_accuracy))

                self.losses_per_epoch.append(np.mean(epoch_losses))
                self.metric_per_epoch.append(np.mean(epoch_metric))
                self.metric_per_epoch_test.append(np.mean(epoch_metric_test))

                progress_bar.close()

        except KeyboardInterrupt:

            if progress_bar:
                progress_bar.close()

    @staticmethod
    def batch_processing(batch):

        x, y = batch

        x = x.view(x.shape[0], -1).numpy()
        y = y.numpy()

        return x, y

    def train_batch(self, x, y):
        raise NotImplementedError

    def predict_batch(self, x):
        return self.model.forward(x)[:, 1]

    def plot(self):

        plt.figure(figsize=(16, 12))

        plt.subplot(1, 2, 1)

        plt.grid()
        plt.xlabel("Training step", fontsize=12)
        plt.ylabel("Loss", fontsize=12)
        plt.plot(self.losses)

        plt.subplot(1, 2, 2)

        plt.grid()
        plt.xlabel("Epoch", fontsize=12)
        plt.ylabel("Metric", fontsize=12)
        plt.plot(self.metric_per_epoch, label="Train")
        plt.plot(self.metric_per_epoch_test, label="Valid")
        plt.ylim(0, 1)
        plt.legend()

        plt.show()


class MNISTWrapper(Wrapper):
    def __init__(self, model, loss, learning_rate=0.001, multi_class=False):

        # ???????????????? ??????????????????, ?????????? ?????????????????? __init__ ???? ???????????????????????? ????????????
        # ?????????? ???????? ???? ?????????????? ?????????? **kwargs, ???? ???????????? ?????? ?????? ?????????????????????? ?? ?????????? ???????? ?????????????????? ?? ??????????????

        super().__init__(
            model=model, loss=loss, learning_rate=learning_rate, multi_class=multi_class
        )

    def train_batch(self, x, y):
        """
        ?????????? ?????????????????????? ???????? ???????????????? ???????????????? ????????????:
        1. ?????????????? forward
        2. ?????????????? ?????????????? ????????????
        3. ?????????????? backward ???? ?????????????? ????????????
        4. ?????????????? backward ???? ????????????
        5. ???????????????????? ??????????
        :param x: ?????????????? ???????????? np.array with shape (batch_size, n_features)
        :param y: ???????????????????????? np.array with shape (batch_size, n_classes)
        :return:
        loss_batch - ???????????????? ?????????????? ????????????, ???????????? ????????????
        prediction - ?????????????? ???????????????????????? ?????????? ????????????

        ?????????????? ???????????? ??????????, ?????????????? ?????????? ?????? ??????????:
        self.model
        self.loss
        self.learning_rate
        """
        ...

    def predict_batch(self, x):
        """
        ???????????????????????? (aka inference) ?????????? ????????????:
        1. ?????????????? forward
        :param x: ?????????????? ???????????? np.array with shape (batch_size, n_features)
        :return: prediction - ?????????????? ???????????????????????? ?????????? ????????????
        """
        ...
