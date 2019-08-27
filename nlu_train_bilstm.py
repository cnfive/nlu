import tensorflow as tf
import json
#import jieba
import numpy as np
from numpy import mat,matrix,shape

def get_features(file_path):
    with open(file_path, 'r') as f:
        data_list = json.load(f)
    #print(data_list)
    domain_value_list = []
    intent_value_list = []
    slots_key_list = []
    slots_value_list = []
    for data in data_list:
        print(data)
        domain_value = data['domain']
        intent_value = data['intent']
        if 'slots' not in data.keys():
            print(data)
            continue
        else:
            slots = data['slots']
            if type(slots) != dict:
                slots = {}
                print(slots)
                continue

        if domain_value not in domain_value_list:
            domain_value_list.append(domain_value)

        if intent_value not in intent_value_list:
            intent_value_list.append(intent_value)

        for key, value in slots.items():
            if key not in slots_key_list:
                slots_key_list.append(key)
            if value not in slots_value_list:
                slots_value_list.append(value)

    return domain_value_list, intent_value_list, slots_key_list, slots_value_list

def eming(filepath,slots_key_dic):

    file1="./new_vocab.txt"
    vocab=open(file1,"r")
    dic={}
    max_length=30
    for line in vocab:

        # print(line)
         word_seq=line.split("	")
        # print(word_seq[0]+"---")
        # print(word_seq[1].strip()+"---")

         dic[word_seq[0].strip()]=word_seq[1].strip()
   # print(dic)
  #  input()

    string_list=[]
    domain_list_id=[]
    data=open(filepath,"r")
    data_list = json.load(data)
    slot_word_index=[]
   
    for line in data_list:
     if len(line["text"])<=30:
        #print(line["text"])
        #string_list=[]
        seg_list =line["text"]

      #  seg_list = jieba.cut(line["text"])
       # seq=" ".join(seg_list)
       # print(seq)

        id_list=[]
        id_list.append(dic['[CLS]'])
        for s in seg_list:
             #  print(s)
               if s==' ':
                    s="blank"
               print(dic[s])
               id_list.append(dic[s])

        id_list.append(dic['[SEP]'])  

        if len(seg_list)<max_length:
             for step in range(max_length-len(seg_list)):


                  id_list.append(dic["[PAD]"])


       # print(id_list)
        #print("len:",len(id_list))
       # input()
        string_list.append(id_list)

        #em_list=bc.encode(string_list)
        #print(em_list)
       # em_list_all.append(em_list)
        domain_list_id.append(domiain_dic[line["domain"]])

        slots=line["slots"]
        word_index=[]
        word_index.append(0)

        for i in  range(max_length):

              word_index.append(0)

        if len(slots)>0:
          # print(slots)
           for key in slots:
                 word=slots[key].strip()
                 index=line["text"].index(word)
                 count=len(word)

           #      print(word)

                 for i in range(count):
                       word_index[index+i]=slots_key_dic[key]
              
        word_index.append(0)
        #print(line["text"])
       # print(word_index)
        #input()
        slot_word_index.append(word_index)

    return string_list,domain_list_id,slot_word_index

def weight(shape, stddev=0.1, mean=0):
    initial = tf.truncated_normal(shape=shape, mean=mean, stddev=stddev)
    return tf.Variable(initial)


def bias(shape, value=0.1):
    initial = tf.constant(value=value, shape=shape)
    return tf.Variable(initial)


def lstm_cell(num_units, keep_prob=0.95):
    cell = tf.nn.rnn_cell.LSTMCell(num_units, reuse=tf.AUTO_REUSE)
    return tf.nn.rnn_cell.DropoutWrapper(cell, output_keep_prob=keep_prob)



if __name__=="__main__":
       domain_value_list, intent_value_list, slots_key_list, slots_value_list=get_features("./train.json")
       domiain_dic={}
       num=0
       max_acc=0

       for domiain in domain_value_list:

               domiain_dic[domiain]=num
               num=num+1

     #  print(domiain_dic)
       slots_key_dic={}
       num=1

       for key in slots_key_list:
             
          slots_key_dic[key]=num
          num=num+1

       slots_key_dic["pad"]=0

       em_list_all,domain_list_id,slot_word_index=eming("./train.json",slots_key_dic)
      # print("hello  world")
     #  print(em_list_all)
     #  print(slot_word_index)

       batch_size=256
       
       input_x=[]
       y_t=[]

       for i in range(int(len(em_list_all)/batch_size)):
           list_temp=[]
           list_temp_y=[]

           for key in range(batch_size): 

                list_temp.append(em_list_all[key+i*batch_size])
                
                print(em_list_all[key+i*batch_size])
                list_temp_y.append(slot_word_index[key+i*batch_size])

         #  print("i=",i)
         #  print("batch_size=",batch_size)
         #  print(type(list_temp))
         ##  print(shape(list_temp))
           
           #m=matrix(list_temp)

           mf=np.reshape(list_temp,[batch_size,32])

           input_x.append(list_temp)

           y_t.append(list_temp_y)

       #print(input_x)
       #x=input_x


       learning_rate=0.01

       global_step = tf.Variable(-1, trainable=False, name='global_step')

       num_layer=1

       num_units=1280

       y_label=tf.placeholder(dtype=tf.float32, shape=[None,32])

#shu chu fen lei shu mu
       category_num=len(slots_key_dic)
#print(word_dic)
       print("category_num:",category_num)


       n_steps=1
       x_input=tf.placeholder(dtype=tf.float32, shape=[None,n_steps,32])
       keep_prob=0.95

    
  
       cell_fw = [lstm_cell(num_units, keep_prob) for _ in range(num_layer)]
       cell_bw = [lstm_cell(num_units, keep_prob) for _ in range(num_layer)]




     #  print(x_input)
       inputs = tf.unstack(x_input, n_steps, axis=1)
       output, _, _ = tf.contrib.rnn.stack_bidirectional_rnn(cell_fw, cell_bw, inputs, dtype=tf.float32)
       print(len(output))
      # print(output)
       output = tf.stack(output, axis=1)
       print("+++++++++++++++++++++++++++")
       print('Output:', output)


       sentence_length=32

       output2 = tf.reshape(output, [sentence_length*batch_size, -1])

       print('Output Reshape', output2.shape)

       with tf.variable_scope('outputs'):


            w = weight([80, category_num])
            b = bias([category_num])
            print("w:",w.shape)
            print("b:",b.shape)
            print("output2:",output2.shape)

            y2 = tf.matmul(output2, w) + b

            print("y.shape:",y2.shape)

        
            y_predict = tf.cast(tf.argmax(y2, axis=1), tf.int32)
            print('Output Y shape:', y_predict.shape)
       



#对输出标签 定义为1行多列
            y_label_reshape = tf.cast(tf.reshape(y_label, [-1]), tf.int32)
            print('Y Label Reshape', y_label_reshape)
            print("y_predict.shape:",y_predict.shape)
            print("y_label.shape",y_label.shape)
    

    
    # Prediction
       correct_prediction = tf.equal(y_predict, y_label_reshape)
       accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
       #tf.summary.scalar('accuracy', accuracy)
    
       print('Prediction', correct_prediction, 'Accuracy', accuracy)
    
    # Loss
       cross_entropy = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y_label_reshape,logits=tf.cast(y2, tf.float32)))

      # tf.summary.scalar('loss', cross_entropy)
    
# Train
       train = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy, global_step=global_step)
    

       saver = tf.train.Saver(max_to_keep=3)


       count=int(len(em_list_all)/batch_size)
  
       sess=tf.Session()
       sess.run(tf.global_variables_initializer())
       #print("x shape:",len(x))

       #input()
      # model_file=tf.train.latest_checkpoint('nlu_1/')  #载入上一次的模型
      # saver.restore(sess,model_file)

       for j in range(5):

           batch=0
           
           acc_t=0
           loss_t=0

           print("j=",j)

           for i in range(count):

               # print("i=",i)
 
 
               # mf=np.reshape(input_x[i],[batch_size,32])

                mf=tf.reshape(input_x[i],[batch_size,1,32])

               # print("x[i] shape:",mf.shape)

                x_feed=sess.run(mf)

                y_t[i]=tf.reshape(y_t[i],[batch_size,32])

                y_feed=sess.run(y_t[i])

               # print("x_feed:",x_feed.shape)

                _,acc,loss,predict=sess.run([train,accuracy,cross_entropy,y_predict] ,feed_dict={x_input:x_feed,y_label:y_feed})
 
                acc_t=acc_t+acc

               #print(acc)

                loss_t=loss_t+loss

           acc=acc_t/count
           loss=loss_t/count

           print("acc:",acc)
           print("loss:",loss)

           if loss<0.1:
                     print(y_predict)
                     print(y_feed)

                     print("acc:",acc)
                     print("loss:",loss)

           if acc>max_acc:
                 max_acc=acc
           if max_acc>0.9:

                 saver.save(sess,'nlu_1/model.ckpt',global_step=j+1)

      # saver.save(sess,'nlu_1/model.ckpt',global_step=1001)


       
