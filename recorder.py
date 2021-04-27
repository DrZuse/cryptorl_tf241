import asyncio
import time
from datetime import datetime as dt
from multiprocessing import Process
from threading import Timer

from configurations import BASKET, LOGGER, SNAPSHOT_RATE
from data_recorder.coinbase_connector.coinbase_client import CoinbaseClient


class Recorder(Process):

    def __init__(self, symbol):
        """
        Constructor of Recorder.

        :param symbols: basket of securities to record...
                        Example: symbols = [('BTC-USD, 'tBTCUSD')]
        """
        super(Recorder, self).__init__()
        self.symbol = symbol
        self.timer_frequency = SNAPSHOT_RATE
        self.workers = dict()
        self.current_time = dt.now()
        self.daemon = False

    def run(self) -> None:
        """
        New process created to instantiate limit order books for
            (1) Coinbase Pro

        Connections made to each exchange are made asynchronously thanks to asyncio.

        :return: void
        """

        self.workers[self.symbol] = CoinbaseClient(sym=self.symbol)
        self.workers[self.symbol].start()

        Timer(5.0, self.timer_worker, args=(self.workers[self.symbol],)).start()

        tasks = asyncio.gather(*[self.workers[sym].subscribe()
                                 for sym in self.workers.keys()])
        loop = asyncio.get_event_loop()
        LOGGER.info(f'Recorder: Gathered {len(self.workers.keys())} tasks')

        try:
            loop.run_until_complete(tasks)
            loop.close()
            [self.workers[sym].join() for sym in self.workers.keys()]
            LOGGER.info(f'Recorder: loop closed for {self.symbol}.')

        except KeyboardInterrupt as e:
            LOGGER.info(f"Recorder: Caught keyboard interrupt. \n{e}")
            tasks.cancel()
            loop.close()
            [self.workers[sym].join() for sym in self.workers.keys()]

        finally:
            loop.close()
            LOGGER.info(f'Recorder: Finally done for {self.symbol}.')

    def timer_worker(self, coinbaseClient: CoinbaseClient,) -> None:
        """
        Thread worker to be invoked every N seconds (e.g., configurations.SNAPSHOT_RATE)

        :param coinbaseClient: CoinbaseClient
        :return: void
        """
        Timer(self.timer_frequency, self.timer_worker, args=(coinbaseClient,)).start()
        self.current_time = dt.now()

        if coinbaseClient.book.done_warming_up:
            """
            This is the place to insert a trading model. 
            You'll have to create your own.
            
            Example:
                orderbook_data = coinbaseClient.book
                model = agent.dqn.Agent()
                fix_api = SomeFixAPI() 
                action = model(orderbook_data)
                if action is buy:
                    buy_order = create_order(pair, price, etc.)
                    fix_api.send_order(buy_order)
            
            """
            LOGGER.info(f'{coinbaseClient.sym} >> {coinbaseClient.book}')
            # The `render_book()` method returns a numpy array of the LOB's current state,
            # as well as resets the Order Flow Imbalance trackers.
            # The LOB snapshot is in a tabular format with columns as defined in
            # `render_lob_feature_names()`
            _ = coinbaseClient.book.render_book()

        else:
            LOGGER.info('Coinbase is still warming up...')


def main():
    LOGGER.info(f'Starting recorder with basket = {BASKET}')

    Recorder(BASKET).start()
    LOGGER.info(f'Process started up for {BASKET}')
    time.sleep(9)


if __name__ == "__main__":
    """
    Entry point of application
    """
    main()
