from sklearn.metrics import classification_report, confusion_matrix


def get_top1_classification_results(predicted_results, label_dict):
    predicted_results_top1 = []
    for predicted_result in predicted_results:
        probs_result = predicted_result.probs
        prob = probs_result.top1conf.cpu().item()
        label = label_dict[probs_result.top1]
        predicted_results_top1.append({label: prob})
    return predicted_results_top1


def get_top1_evaluation(y_true, y_pred_top1):
    y_pred = [list(pred_dict.keys())[0] for pred_dict in y_pred_top1]
    return dict(classification_report=classification_report(y_true, y_pred, output_dict=True),
                confusion_matrix=confusion_matrix(y_true, y_pred,
                                                  labels=sorted(list(set(y_true)))))


def get_top5_classification_results(predicted_results, label_dict, thresh_hold=0.01):
    predicted_results_top5 = []
    for predicted_result in predicted_results:
        probs_result = predicted_result.probs
        top5_probs = probs_result.top5conf.cpu().numpy()
        probs = [prob for prob in top5_probs if prob >= thresh_hold]
        labels = [label_dict[label] for label in probs_result.top5[:len(probs)]]
        predicted_results_top5.append(dict(zip(labels, probs)))
    return predicted_results_top5


def get_top5_evaluation(y_true, y_pred_top5):
    y_pred = []
    for i, label in enumerate(y_true):
        if label in y_pred_top5[i]:
            y_pred.append(label)
        else:
            result_dict = y_pred_top5[i]
            top1_result = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)[0][0]
            y_pred.append(top1_result)
    return dict(classification_report=classification_report(y_true, y_pred, output_dict=True),
                confusion_matrix=confusion_matrix(y_true, y_pred,
                                                  labels=sorted(list(set(y_true)))))
