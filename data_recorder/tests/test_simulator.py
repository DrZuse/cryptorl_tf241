from datetime import datetime as dt
from datetime import timedelta

from configurations import TIMEZONE, CCY, RECORD_DATA
from data_recorder.database.simulator import Simulator


def test_get_tick_history() -> None:
    """
    Test case to query Arctic TickStore
    """
    start_time = dt.now(tz=TIMEZONE)

    sim = Simulator()
    query = {
        'ccy': CCY,
        'start_date': start_date,
        'end_date': end_date,
    }
    tick_history = sim.db.get_tick_history(query=query)
    print('\n{}\n'.format(tick_history))

    elapsed = (dt.now(tz=TIMEZONE) - start_time).seconds
    print('Completed %s in %i seconds' % (__name__, elapsed))
    print('DONE. EXITING %s' % __name__)


def test_get_orderbook_snapshot_history() -> None:
    """
    Test case to export testing/training data for reinforcement learning
    """
    start_time = dt.now(tz=TIMEZONE)

    sim = Simulator()
    query = {
        'ccy': CCY,
        'start_date': start_date,
        'end_date': end_date,
    }
    orderbook_snapshot_history = sim.get_orderbook_snapshot_history(query=query)
    if orderbook_snapshot_history is None:
        print('Exiting: orderbook_snapshot_history is NONE')
        return

    filename = 'test_' + '{}_{}'.format(query['ccy'][0], query['start_date'])
    sim.export_to_csv(data=orderbook_snapshot_history,
                      filename=filename, compress=False)

    elapsed = (dt.now(tz=TIMEZONE) - start_time).seconds
    print('Completed %s in %i seconds' % (__name__, elapsed))
    print('DONE. EXITING %s' % __name__)


def test_extract_features(start_date, end_date, CCY) -> None:
    """
    Test case to export *multiple* testing/training data sets for reinforcement learning
    """
    start_time = dt.now(tz=TIMEZONE)

    sim = Simulator()

    query = {
        'ccy': CCY,
        'start_date': start_date,
        'end_date': end_date,
    }
    sim.extract_features(query)

    elapsed = (dt.now(tz=TIMEZONE) - start_time).seconds
    print('Completed %s in %i seconds' % (__name__, elapsed))
    print('DONE. EXITING %s' % __name__)


if __name__ == '__main__':
    """
    Entry point of tests application
    """

    yestarday = (dt.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = dt.now().strftime("%Y-%m-%d")
    tomorrow = (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    start_date = yestarday
    end_date = tomorrow


    #start_date = '2021-04-22T15:58:32.362+00:00'
    #end_date = '2021-04-22T16:03:42.054+00:00'

    



    if RECORD_DATA:
        print('please set RECORD_DATA to False')
    else:
        #test_get_tick_history(start_date, end_date, CCY)
        #test_get_orderbook_snapshot_history(start_date, end_date, CCY)
        test_extract_features(start_date, end_date, CCY)
