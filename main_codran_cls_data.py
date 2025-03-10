from data_manager import *
from models.SFTRL_CCFM import SFTRL_CCFM
from models.SFTRL_Vanila import SFTRL_Vanila
from models.FM_FTRL import  FM_FTRL
from models.RRF import RRF
from peformance_manager import *
from sklearn.datasets import load_svmlight_file

#import

if __name__ == "__main__":

    data_dir = './data/cod-rna2/'
    filename = "cod-rna2.scale"
    X, y = load_svmlight_file(data_dir + filename, n_features=8)
    X = X.toarray()

    want_permute = False
    if want_permute :
        idx = np.random.permutation(X.shape[0])
        x_train_s = np.asarray(X[idx])
        rate_train_s = np.asarray(y[idx])
    else:
        x_train_s = np.asarray(X)
        rate_train_s = np.asarray(y)


    down_sampling = 5
    inputs_matrix = torch.tensor(x_train_s[0:x_train_s.size:down_sampling]).double()
    outputs = torch.tensor(rate_train_s[0:x_train_s.size:down_sampling]).double()

    # # model setup

    # c = RRF(loss='l2', task="regression", learning_rate=0.003,
    #         learning_rate_gamma=0.001, gamma=1.0, D=100)
    c = RRF(loss='logit', task="classification", learning_rate=0.003,
            learning_rate_gamma=0.001, gamma=1.0, D=100)


    pred_RRF = c.fit(x_train_s[0:x_train_s.size:down_sampling], rate_train_s[0:x_train_s.size:down_sampling])
    #train_time = c.train_time
    #print(pred_rrf)

    m = 10

    options = {}
    options['Data'] = filename
    options['m']  = m
    options['eta'] = 5e-2
    options['task'] = 'cls'

    options2 = {}
    options2['Data'] = filename
    options2['m']  = m
    options2['eta'] = 5e-2
    options2['task'] = 'cls'

    options3 = {}
    options3['Data'] = filename
    options3['m']  = m
    options3['eta'] = 5e-2
    options3['task'] = 'cls'
    #
    #
    recent_num = -1
    Model_CCFM = SFTRL_CCFM(inputs_matrix[:recent_num ,:] ,outputs[:recent_num] ,options)
    Model_Vanila = SFTRL_Vanila(inputs_matrix[:recent_num ,:] ,outputs[:recent_num] ,options2)
    Model_FM_FTRL = FM_FTRL(inputs_matrix[:recent_num ,:] ,outputs[:recent_num] ,options3)


    pred_C , real = Model_CCFM.online_learning()
    pred_V, _ = Model_Vanila.online_learning()
    pred_F, _ = Model_FM_FTRL.online_learning()


    cls_metric_C,cls_metric_C_cnt = classfication_metric(pred_C, real)
    cls_metric_V,cls_metric_V_cnt = classfication_metric(pred_V, real)
    cls_metric_F,cls_metric_F_cnt = classfication_metric(pred_F, real)
    cls_metric_RRF,cls_metric_RRF_cnt = classfication_metric(pred_RRF, real)


    save_path1 = './figure_results/cod-rna2/pred_cls_'
    save_path2 = './figure_results/cod-rna2/metric_cls_'


    save_legend = ['SFTRL_CCFM', 'SFTRL_Vanila','RRF','FM_FTRL']
    fig_prediction([pred_C,pred_V,pred_RRF,pred_F],save_legend,real,options,save_path1)
    fig_metric_cls([cls_metric_C,cls_metric_V,cls_metric_RRF,cls_metric_F],
                   [cls_metric_C_cnt,cls_metric_V_cnt,cls_metric_RRF_cnt,cls_metric_F_cnt],save_legend,options,save_path2)

