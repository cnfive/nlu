import numpy as np
import tensorflow as tf
from hparams import Hparams
import json


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

def ln(inputs, epsilon = 1e-8, scope="ln"):
    '''Applies layer normalization. See https://arxiv.org/abs/1607.06450.
    inputs: A tensor with 2 or more dimensions, where the first dimension has `batch_size`.
    epsilon: A floating number. A very small number for preventing ZeroDivision Error.
    scope: Optional scope for `variable_scope`.
      
    Returns:
      A tensor with the same shape and data dtype as `inputs`.
    '''
    with tf.variable_scope(scope, reuse=tf.AUTO_REUSE):
        inputs_shape = inputs.get_shape()
        params_shape = inputs_shape[-1:]
    
        mean, variance = tf.nn.moments(inputs, [-1], keep_dims=True)
        beta= tf.get_variable("beta", params_shape, initializer=tf.zeros_initializer())
        gamma = tf.get_variable("gamma", params_shape, initializer=tf.ones_initializer())
        normalized = (inputs - mean) / ( (variance + epsilon) ** (.5) )
        outputs = gamma * normalized + beta
        
    return outputs


def get_token_embeddings(vocab_size, num_units, zero_pad=True):
    '''Constructs token embedding matrix.
    Note that the column of index 0's are set to zeros.
    vocab_size: scalar. V.
    num_units: embedding dimensionalty. E.
    zero_pad: Boolean. If True, all the values of the first row (id = 0) should be constant zero
    To apply query/key masks easily, zero pad is turned on.

    Returns
    weight variable: (V, E)
    '''
    with tf.variable_scope("shared_weight_matrix"):
        embeddings = tf.get_variable('weight_mat',
                                   dtype=tf.float32,
                                   shape=(vocab_size, num_units),
                                   initializer=tf.contrib.layers.xavier_initializer())
        if zero_pad:
            embeddings = tf.concat((tf.zeros(shape=[1, num_units]),
                                    embeddings[1:, :]), 0)
    return embeddings


def scaled_dot_product_attention(Q, K, V,
                                 causality=False, dropout_rate=0.,
                                 training=True,
                                 scope="scaled_dot_product_attention"):
    '''See 3.2.1.
    Q: Packed queries. 3d tensor. [N, T_q, d_k].
    K: Packed keys. 3d tensor. [N, T_k, d_k].
    V: Packed values. 3d tensor. [N, T_k, d_v].
    causality: If True, applies masking for future blinding
    dropout_rate: A floating point number of [0, 1].
    training: boolean for controlling droput
    scope: Optional scope for `variable_scope`.
    '''
    with tf.variable_scope(scope, reuse=tf.AUTO_REUSE):
        d_k = Q.get_shape().as_list()[-1]

        # dot product
        outputs = tf.matmul(Q, tf.transpose(K, [0, 2, 1]))  # (N, T_q, T_k)

        # scale
        outputs /= d_k ** 0.5

        # key masking
        outputs = mask(outputs, Q, K, type="key")

        # causality or future blinding masking
        if causality:
            outputs = mask(outputs, type="future")

        # softmax
        outputs = tf.nn.softmax(outputs)
        attention = tf.transpose(outputs, [0, 2, 1])
        tf.summary.image("attention", tf.expand_dims(attention[:1], -1))

        # query masking
        outputs = mask(outputs, Q, K, type="query")

        # dropout
        outputs = tf.layers.dropout(outputs, rate=dropout_rate, training=training)

        # weighted sum (context vectors)
        outputs = tf.matmul(outputs, V)  # (N, T_q, d_v)

    return outputs


def mask(inputs, queries=None, keys=None, type=None):
    """Masks paddings on keys or queries to inputs
    inputs: 3d tensor. (N, T_q, T_k)
    queries: 3d tensor. (N, T_q, d)
    keys: 3d tensor. (N, T_k, d)

    e.g.,
    >> queries = tf.constant([[[1.],
                        [2.],
                        [0.]]], tf.float32) # (1, 3, 1)
    >> keys = tf.constant([[[4.],
                     [0.]]], tf.float32)  # (1, 2, 1)
    >> inputs = tf.constant([[[4., 0.],
                               [8., 0.],
                               [0., 0.]]], tf.float32)
    >> mask(inputs, queries, keys, "key")
    array([[[ 4.0000000e+00, -4.2949673e+09],
        [ 8.0000000e+00, -4.2949673e+09],
        [ 0.0000000e+00, -4.2949673e+09]]], dtype=float32)
    >> inputs = tf.constant([[[1., 0.],
                             [1., 0.],
                              [1., 0.]]], tf.float32)
    >> mask(inputs, queries, keys, "query")
    array([[[1., 0.],
        [1., 0.],
        [0., 0.]]], dtype=float32)
    """
    padding_num = -2 ** 32 + 1
    if type in ("k", "key", "keys"):
        # Generate masks
        masks = tf.sign(tf.reduce_sum(tf.abs(keys), axis=-1))  # (N, T_k)
        masks = tf.expand_dims(masks, 1) # (N, 1, T_k)
        masks = tf.tile(masks, [1, tf.shape(queries)[1], 1])  # (N, T_q, T_k)

        # Apply masks to inputs
        paddings = tf.ones_like(inputs) * padding_num
        outputs = tf.where(tf.equal(masks, 0), paddings, inputs)  # (N, T_q, T_k)
    elif type in ("q", "query", "queries"):
        # Generate masks
        masks = tf.sign(tf.reduce_sum(tf.abs(queries), axis=-1))  # (N, T_q)
        masks = tf.expand_dims(masks, -1)  # (N, T_q, 1)
        masks = tf.tile(masks, [1, 1, tf.shape(keys)[1]])  # (N, T_q, T_k)

        # Apply masks to inputs
        outputs = inputs*masks
    elif type in ("f", "future", "right"):
        diag_vals = tf.ones_like(inputs[0, :, :])  # (T_q, T_k)
        tril = tf.linalg.LinearOperatorLowerTriangular(diag_vals).to_dense()  # (T_q, T_k)
        masks = tf.tile(tf.expand_dims(tril, 0), [tf.shape(inputs)[0], 1, 1])  # (N, T_q, T_k)

        paddings = tf.ones_like(masks) * padding_num
        outputs = tf.where(tf.equal(masks, 0), paddings, inputs)
    else:
        print("Check if you entered type correctly!")


    return outputs

def multihead_attention(queries, keys, values,
                        num_heads=8, 
                        dropout_rate=0,
                        training=True,
                        causality=False,
                        scope="multihead_attention"):
    '''Applies multihead attention. See 3.2.2
    queries: A 3d tensor with shape of [N, T_q, d_model].
    keys: A 3d tensor with shape of [N, T_k, d_model].
    values: A 3d tensor with shape of [N, T_k, d_model].
    num_heads: An int. Number of heads.
    dropout_rate: A floating point number.
    training: Boolean. Controller of mechanism for dropout.
    causality: Boolean. If true, units that reference the future are masked.
    scope: Optional scope for `variable_scope`.
        
    Returns
      A 3d tensor with shape of (N, T_q, C)  
    '''
    d_model = queries.get_shape().as_list()[-1]
    with tf.variable_scope(scope, reuse=tf.AUTO_REUSE):
        # Linear projections
        Q = tf.layers.dense(queries, d_model, use_bias=False) # (N, T_q, d_model)
        K = tf.layers.dense(keys, d_model, use_bias=False) # (N, T_k, d_model)
        V = tf.layers.dense(values, d_model, use_bias=False) # (N, T_k, d_model)
        
        # Split and concat
        Q_ = tf.concat(tf.split(Q, num_heads, axis=2), axis=0) # (h*N, T_q, d_model/h)
        K_ = tf.concat(tf.split(K, num_heads, axis=2), axis=0) # (h*N, T_k, d_model/h)
        V_ = tf.concat(tf.split(V, num_heads, axis=2), axis=0) # (h*N, T_k, d_model/h)

        # Attention
        outputs = scaled_dot_product_attention(Q_, K_, V_, causality, dropout_rate, training)

        # Restore shape
        outputs = tf.concat(tf.split(outputs, num_heads, axis=0), axis=2 ) # (N, T_q, d_model)
              
        # Residual connection
        outputs += queries
              
        # Normalize
        outputs = ln(outputs)
 
    return outputs


def ff(inputs, num_units, scope="positionwise_feedforward"):
    '''position-wise feed forward net. See 3.3
    
    inputs: A 3d tensor with shape of [N, T, C].
    num_units: A list of two integers.
    scope: Optional scope for `variable_scope`.

    Returns:
      A 3d tensor with the same shape and dtype as inputs
    '''
    with tf.variable_scope(scope, reuse=tf.AUTO_REUSE):
        # Inner layer
        outputs = tf.layers.dense(inputs, num_units[0], activation=tf.nn.relu)

        # Outer layer
        outputs = tf.layers.dense(outputs, num_units[1])

        # Residual connection
        outputs += inputs
        
        # Normalize
        outputs = ln(outputs)
    
    return outputs


def label_smoothing(inputs, epsilon=0.1):
    '''Applies label smoothing. See 5.4 and https://arxiv.org/abs/1512.00567.
    inputs: 3d tensor. [N, T, V], where V is the number of vocabulary.
    epsilon: Smoothing rate.
    
    For example,
    
    ```
    import tensorflow as tf
    inputs = tf.convert_to_tensor([[[0, 0, 1], 
       [0, 1, 0],
       [1, 0, 0]],

      [[1, 0, 0],
       [1, 0, 0],
       [0, 1, 0]]], tf.float32)
       
    outputs = label_smoothing(inputs)
    
    with tf.Session() as sess:
        print(sess.run([outputs]))
    
    >>
    [array([[[ 0.03333334,  0.03333334,  0.93333334],
        [ 0.03333334,  0.93333334,  0.03333334],
        [ 0.93333334,  0.03333334,  0.03333334]],

       [[ 0.93333334,  0.03333334,  0.03333334],
        [ 0.93333334,  0.03333334,  0.03333334],
        [ 0.03333334,  0.93333334,  0.03333334]]], dtype=float32)]   
    ```    
    '''
    #inputs=tf.cast(inputs,dtype=tf.int32)

    V = inputs.get_shape().as_list()[-1] # number of channels
    return ((1-epsilon) * inputs) + (epsilon /V)
    
def positional_encoding(inputs,
                        maxlen,
                        masking=True,
                        scope="positional_encoding"):
    '''Sinusoidal Positional_Encoding. See 3.5
    inputs: 3d tensor. (N, T, E)
    maxlen: scalar. Must be >= T
    masking: Boolean. If True, padding positions are set to zeros.
    scope: Optional scope for `variable_scope`.

    returns
    3d tensor that has the same shape as inputs.
    '''

    E = inputs.get_shape().as_list()[-1] # static
    N, T = tf.shape(inputs)[0], tf.shape(inputs)[1] # dynamic
    with tf.variable_scope(scope, reuse=tf.AUTO_REUSE):
        # position indices
        position_ind = tf.tile(tf.expand_dims(tf.range(T), 0), [N, 1]) # (N, T)

        # First part of the PE function: sin and cos argument
        position_enc = np.array([
            [pos / np.power(10000, (i-i%2)/E) for i in range(E)]
            for pos in range(maxlen)])

        # Second part, apply the cosine to even columns and sin to odds.
        position_enc[:, 0::2] = np.sin(position_enc[:, 0::2])  # dim 2i
        position_enc[:, 1::2] = np.cos(position_enc[:, 1::2])  # dim 2i+1
        position_enc = tf.convert_to_tensor(position_enc, tf.float32) # (maxlen, E)

        # lookup
        outputs = tf.nn.embedding_lookup(position_enc, position_ind)

        # masks
        if masking:
            outputs = tf.where(tf.equal(inputs, 0), inputs, outputs)

        return tf.to_float(outputs)


def noam_scheme(init_lr, global_step, warmup_steps=4000.):
    '''Noam scheme learning rate decay
    init_lr: initial learning rate. scalar.
    global_step: scalar.
    warmup_steps: scalar. During warmup_steps, learning rate increases
        until it reaches init_lr.
    '''
    step = tf.cast(global_step + 1, dtype=tf.float32)
    return init_lr * warmup_steps ** 0.5 * tf.minimum(step * warmup_steps ** -1.5, step ** -0.5)


def encode(xs, training=True):
        '''
        Returns
        memory: encoder outputs. (N, T1, d_model)
        '''
        with tf.variable_scope("encoder", reuse=tf.AUTO_REUSE):
           # x, seqlens, sents1 = xs
            x =  tf.cast(xs,dtype=tf.int32)
            # embedding
            enc = tf.nn.embedding_lookup(embeddings, x) # (N, T1, d_model)
            enc *= d_model**0.5 # scale

            enc += positional_encoding(enc, maxlen1)
            enc = tf.layers.dropout(enc,dropout_rate, training=training)

            ## Blocks
            for i in range(num_blocks):
                with tf.variable_scope("num_blocks_{}".format(i), reuse=tf.AUTO_REUSE):
                    # self-attention
                    enc = multihead_attention(queries=enc,
                                              keys=enc,
                                              values=enc,
                                              num_heads=num_heads,
                                              dropout_rate=dropout_rate,
                                              training=training,
                                              causality=False)
                    # feed forward
                    enc = ff(enc, num_units=[d_ff, d_model])
        memory = enc
        return memory #, sents1

def decode( ys, memory, training=True):
        '''
        memory: encoder outputs. (N, T1, d_model)

        Returns
        logits: (N, T2, V). float32.
        y_hat: (N, T2). int32
        y: (N, T2). int32
        sents2: (N,). string.
        '''
        with tf.variable_scope("decoder", reuse=tf.AUTO_REUSE):
            #decoder_inputs, y, seqlens, sents2 = ys

            decoder_inputs=tf.cast(ys,dtype=tf.int32)
            # embedding
            dec = tf.nn.embedding_lookup(embeddings, decoder_inputs)  # (N, T2, d_model)
            dec *= d_model ** 0.5  # scale

            dec += positional_encoding(dec, maxlen2)
            dec = tf.layers.dropout(dec, dropout_rate, training=training)

            # Blocks
            for i in range(num_blocks):
                with tf.variable_scope("num_blocks_{}".format(i), reuse=tf.AUTO_REUSE):
                    # Masked self-attention (Note that causality is True at this time)
                    dec = multihead_attention(queries=dec,
                                              keys=dec,
                                              values=dec,
                                              num_heads=num_heads,
                                              dropout_rate=dropout_rate,
                                              training=training,
                                              causality=True,
                                              scope="self_attention")

                    # Vanilla attention
                    dec = multihead_attention(queries=dec,
                                              keys=memory,
                                              values=memory,
                                              num_heads=num_heads,
                                              dropout_rate=dropout_rate,
                                              training=training,
                                              causality=False,
                                              scope="vanilla_attention")
                    ### Feed Forward
                    dec = ff(dec, num_units=[d_ff, d_model])

        # Final linear projection (embedding weights are shared)
        weights = tf.transpose(embeddings) # (d_model, vocab_size)
        logits = tf.einsum('ntd,dk->ntk', dec, weights) # (N, T2, vocab_size)
        y_hat = tf.to_int32(tf.argmax(logits, axis=-1))

        return logits, y_hat#, y  #, sents2

def train(xs):
        '''
        Returns
        loss: scalar.
        train_op: training operation
        global_step: scalar.
        summaries: training summary node
        '''
        # forward
   # memory, sents1 = encode(xs)
        memory= encode(xs)
    #logits, preds, y, sents2 = self.decode(ys, memory)


if __name__=="__main__":
       xs=tf.placeholder(dtype=tf.float32, shape=[None,32])

       ys=tf.placeholder(dtype=tf.float32, shape=[None,32])

       vocab_size=8820
       d_model=64
       dropout_rate=0.3

       num_blocks=6
       num_heads=8
       d_ff=128

       maxlen1=32
       maxlen2=32
       warmup_steps=400
       lr=0.0003


       domain_value_list, intent_value_list, slots_key_list, slots_value_list=get_features("./train.json")

       #print((slots_key_list))
       #input()
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

       count=int(len(em_list_all)/batch_size)

       #get_token_embeddings(self.vocab_size, self.d_model, zero_pad=True)

       embeddings = get_token_embeddings(vocab_size, d_model, zero_pad=True)


       print(embeddings)

       memory= encode(xs)

    #   decoder_input, y = y[:-1], y[1:]
       logits, preds = decode(ys, memory)

       # train scheme
      # y_ = label_smoothing(tf.one_hot(ys, depth=vocab_size))
      # y_label_reshape = tf.cast(tf.reshape(ys, [-1]), tf.int32)

       d_inputs=tf.cast(ys,dtype=tf.int32)
       y_hot=tf.one_hot(d_inputs, depth=vocab_size)
       y_ = label_smoothing(y_hot)

     
       ce = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_,logits=logits )
       nonpadding = tf.to_float(tf.not_equal(ys, 0))  # 0: <pad>
       loss = tf.reduce_sum(ce * nonpadding) / (tf.reduce_sum(nonpadding) + 1e-7)
     #  loss=tf.reduce_mean(ce)
       global_step = tf.train.get_or_create_global_step()
       #global_steps = tf.Variable(0, trainable=False)
      # global_step = tf.Variable(-1, trainable=False, name='global_step')

      # learning_rate = tf.train.exponential_decay(0.1, global_steps, 10, 2, staircase=False)

       lr = noam_scheme(lr, global_step, warmup_steps)
       #optimizer = tf.train.AdamOptimizer(lr)
       #train_op = optimizer.minimize(loss, global_step=global_steps)
       train_op = tf.train.AdamOptimizer(lr).minimize(loss, global_step=global_step)
      # opt = tf.train.GradientDescentOptimizer(learning_rate=0.001)
      # train_op = opt.minimize(loss)
 # memory, sents1 = encode(xs)
       sess=tf.Session()
      # sess.run(tf.zero_initializer())
       sess.run(tf.global_variables_initializer())
       #print("x shape:",len(x))

       #input()
       #model_file=tf.train.latest_checkpoint('nlu_1/')  #载入上一次的模型
      # saver.restore(sess,model_file)

       for j in range(6):

           batch=0
           
           acc_t=0
           loss_t=0

           print("j=",j)

           for i in range(count):

               # print("i=",i)
 
 
               # mf=np.reshape(input_x[i],[batch_size,32])

                mf=tf.reshape(input_x[i],[batch_size,32])

               # print("x[i] shape:",mf.shape)

                x_feed=sess.run(mf)

                y_t[i]=tf.reshape(y_t[i],[batch_size,32])

                y_feed=sess.run(y_t[i])

               # print("x_feed:",x_feed.shape)

                l,_=sess.run([loss,train_op] ,feed_dict={xs:x_feed,ys:y_feed})
                print(l)
 
