import random
import argparse

ET_ratio_list = [15]
U_list = [45]

for ET_ratio in ET_ratio_list:
    for U in U_list:
        runnable_number = 1000

        BCAT_list = []
        WCAT_list = []
        BCET_list = []
        WCET_list = []
        DDL_list = []
        priority_list = []
        ET_list = []

        for i in range(runnable_number):
            ET_list.append(0 if random.randint(0, 99) < 100-ET_ratio else 1)
            BCAT = random.randint(1, 9900)
            BCAT_list.append(BCAT)
            WCAT_list.append(BCAT + random.randint(0, 9))
            # BCAT_list.append(0 if ET_list[-1] == 1 else BCAT)
            # WCAT_list.append(0 if ET_list[-1] == 1 else BCAT + random.randint(0, 9))
            BCET = random.randint(2, int(U/5-7))
            BCET_list.append(BCET)
            WCET_list.append(BCET + random.randint(1, 4))
            DDL_list.append(10000)
            priority_list.append(random.randint(1, 10))

        with open("./tests/generate_result.txt","w") as dot_file:
            for i in range(runnable_number):
                dot_file.write(str(BCAT_list[i]) + ' ' + str(WCAT_list[i]) + ' ' + str(BCET_list[i]) + ' ' + str(WCET_list[i]) + \
                    ' ' + str(DDL_list[i]) + ' ' + str(priority_list[i]) + ' ' + str(ET_list[i]) + '\n')
        print("Generate input file successfully!")
        print("U = ", sum(WCET_list)/10000)

# def int_or_int_list(value):
#     try:
#         return int(value)
#     except ValueError:
#         return [int(i) for i in value.split(',')]
     
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Generate a network dataset")
#     parser.add_argument("--num_ins", type=int, default=1, help="Number of instances")
#     parser.add_argument("--num_stream", type=int_or_int_list, default=8, help="Number of streams")
#     parser.add_argument("--num_sw", type=int_or_int_list, default=8, help="Number of switches")
#     parser.add_argument(
#         "--period",
#         type=int_or_int_list,
#         default=1,
#         help="Period specification",
#     )
#     parser.add_argument(
#         "--size",
#         type=int_or_int_list,
#         default=2,
#         help="Size specification",
#     )
#     parser.add_argument(
#         "--deadline",
#         type=int_or_int_list,
#         default=1,
#         help="Deadline specification",
#     )
#     parser.add_argument(
#         "--topo",
#         type=int_or_int_list,
#         default=0,
#         help="Topology type: 0-Line, 1-Ring, 2-Tree, 3-Mesh",
#     )
#     parser.add_argument(
#         "--output",
#         type=str,
#         default="./",
#         help="Output folder path",
#     )

#     args = parser.parse_args()
#     generator = DatasetGenerator(
#         args.num_ins,
#         args.num_stream,
#         args.num_sw,
#         args.period,
#         args.size,
#         args.deadline,
#         args.topo,
#     )
#     generator.run(args.output)